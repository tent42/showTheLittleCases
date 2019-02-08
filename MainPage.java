package com.hzdracom.android.framework.page;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

import logic.extenal.android.contact.RawContactReadAllSimTask;
import logic.external.android.x.base.AbstractUIPage;
import logic.external.android.x.base.ContactTask;
import logic.io.socket.protocol.SimpleXmlHelper;
import logic.shared.local.data.SharedStatic;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.database.Cursor;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.provider.ContactsContract.Contacts;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import base.tina.core.task.infc.ITaskResult;
import com.lectek.android.ecp.plugin.contactsbackup.R;
import com.hzdracom.android.framework.dialog.AlertDialogs;
import com.hzdracom.android.framework.dialog.ProgressBackupDialog;
import com.hzdracom.android.framework.dialog.ProgressRecoveryDialog;
import com.lectek.android.ecp.plugin.contactsbackup.MainFrontActivity;
import com.tgx.tina.android.ipc.framework.IUIPage;

public class MainPage 
		extends
		AbstractUIPage<MainFrontActivity>
{
	public Bundle workMession;
	MainFrontActivity t;
	ProgressBackupDialog backup_dialog;
	ProgressRecoveryDialog recovery_dialog;
	public MainPage(MainFrontActivity t) {
		super(t);
		this.t = t;
	}

	@Override
	public <T extends Activity> View createView(T t, int initializers) {
		initConsts();
		curMyView = LayoutInflater.from(context).inflate(R.layout.contact_backup_main, null);
		initView();
		setListener();
		return null;
	}

	@Override
	public View updateView(int toStatus, ITaskResult data) {
		return null;
	}

	Bundle alert = new Bundle();
	@SuppressLint("SimpleDateFormat")
	@Override
	public void notifyView(int cmd, Bundle bundle) {
		switch (cmd) {
		case SharedStatic.Http_Failed:
			alert.putString(SharedStatic.showText, "数据备份阶段的网络异常");
			AlertDialogs ad_Http_Failed = new AlertDialogs(t,R.style.Contact_Dialog,bundle);
			ad_Http_Failed.show();
			t.addDialogtoList(ad_Http_Failed);
		case SharedStatic.Read_Failed:
			AlertDialogs ad_Read_Failed = new AlertDialogs(t,R.style.Contact_Dialog,bundle);
			ad_Read_Failed.show();
			t.addDialogtoList(ad_Read_Failed);
			break;
		case SharedStatic.Download_Failed:
			alert.putString(SharedStatic.showText, "采集失败，对您造成的不便深感抱歉，请重试:)");
			AlertDialogs ad_Download_Failed = new AlertDialogs(t, R.style.Contact_Dialog,alert);
			ad_Download_Failed.show();
			t.addDialogtoList(ad_Download_Failed);
		case SharedStatic.Backup_Sucess:
			secondMessage.setText("云端"+bundle.getInt(SharedStatic.CloudNum)+"个联系人");
			SimpleDateFormat formatter = new SimpleDateFormat("yyyy年MM月dd日    HH:mm:ss     ");
			Date curDate = new Date(System.currentTimeMillis());// 获取当前时间
			String str = formatter.format(curDate);
			firstMessage.setText(""+ str);
			try {
				FileOutputStream fos = context.openFileOutput(ContactTask.TMP_FILE_FOR_REMEND, Context.MODE_PRIVATE);
				DataOutputStream dos = new DataOutputStream(fos);
				StringBuilder sb = new StringBuilder(); 
				sb.append("<xml>");
					sb.append("<time>");
						sb.append(str);
					sb.append("</time>");
					sb.append("<cloud>");
						sb.append(bundle.getInt(SharedStatic.CloudNum));
					sb.append("</cloud>");
				sb.append("</xml>");
				str = sb.toString();
				byte[] info = str.getBytes();
				dos.writeInt(info.length);
				Log.d(getClass().getSimpleName(), info.length+"   ..info.lenght");
				dos.write(info);

				dos.close();
				fos.close();
				
				DataInputStream dis = new DataInputStream(context.openFileInput(ContactTask.TMP_FILE_FOR_REMEND));
				info = new byte[dis.readInt()];
				dis.read(info);
				str = new String(info);
				Log.d(getClass().getSimpleName(), str);
			} catch (Exception e) {
				e.printStackTrace();
				Log.d(getClass().getSimpleName(),"dataoutput  is  error");
			}
			AlertDialogs ad2_Backup_Sucess = new AlertDialogs(t,R.style.Contact_Dialog,bundle);
			ad2_Backup_Sucess.show();
			t.addDialogtoList(ad2_Backup_Sucess);
			
			break;
		case SharedStatic.RecoverystoBackup_Sucess:
			if(recovery_dialog != null){
				recovery_dialog.refreshView(cmd, bundle);
			}
			break;
		case SharedStatic.Backup_Finish:
			if(backup_dialog != null && backup_dialog.readContactAction != null){
				backup_dialog.readContactAction.finish();
			}
			if(recovery_dialog != null && recovery_dialog.writeContact != null){
				recovery_dialog.writeContact.finish();
			}
			break;
		default:
			if(backup_dialog != null ){
				backup_dialog.refreshView(cmd, bundle);
			}
			if(recovery_dialog != null){
				recovery_dialog.refreshView(cmd, bundle);
			}
			
			if(backup_dialog == null && recovery_dialog == null){
				AlertDialogs ab_null = new AlertDialogs(t,R.style.Contact_Dialog,null);
				ab_null.show();
				t.addDialogtoList(ab_null);
			}
			
			break;
		}
	}

	@Override
	public int enter(IUIPage<?> prePage) {
		//t.ioAService.requestService(new HttpTask(new ContactBackUpPlugin(SharedStatic.httpurl)), false);
		int count = countContact(t);
		count += RawContactReadAllSimTask.available;
		//云端联系人
		secondTitle.setText("本地有效"+count+"个联系人  ， ");
		secondMessage.setText("云端"+0+"个联系人");
		
		try {/*
			DataInputStream dis = new DataInputStream(context.openFileInput(ContactTask.TMP_FILE_FOR_REMEND));
			dis.skip(0);
			int len = dis.readInt();
			byte[] info = new byte[len];
			String str = new String();
			dis.read(info);
			str = info.toString();
			if(str != null && !str.equals("")){
				Log.d(getClass().getSimpleName(),str);
				String times = SimpleXmlHelper.getTagValue(str, "time");
				if(times != null && !times.equals("")){
					firstMessage.setText("备份时间"+times);
				}
				String numbers = SimpleXmlHelper.getTagValue(str, "cloud");
				if(numbers != null && !numbers.equals("")){
					secondMessage.setText("云端"+numbers+"个联系人");
				}
			}else{
				firstMessage.setText("您还没有备份记录");
			}
		*/} catch (Exception e) {
			e.printStackTrace();
		}
		return 0;
	}

	@Override
	public int leave(IUIPage<?> nextPage) {
		return 0;
	}

	@Override
	public void setStatus(int status) {
		
	}
	
	/** views */
	public Button btn_contact_backup, btn_contact_recovery;
	public TextView firstTitle , firstMessage
					,secondTitle,secondMessage;
	public ImageButton imageButton_back;
	private void initView(){
		/** set some text  */
		firstTitle = (TextView)curMyView.findViewById(R.id.contact_backup_textView_firstTitle);
		firstTitle.setText(R.string.lastbackup_date);
		firstMessage = (TextView)curMyView.findViewById(R.id.contact_backup_textView_firstMessage);
		secondTitle = (TextView)curMyView.findViewById(R.id.contact_backup_textView_SecondTitle);
		secondMessage = (TextView)curMyView.findViewById(R.id.contact_backup_textView_SecondMessage);
		imageButton_back = (ImageButton)curMyView.findViewById(R.id.contact_selected_back_ImageButton);
		/**  button event set here */
		btn_contact_backup = (Button)curMyView.findViewById(R.id.contact_backup_btn);
		btn_contact_recovery = (Button)curMyView.findViewById(R.id.contact_recovery_btn);
	}
	
	private void initConsts(){
		workMession = new Bundle();
	}
	
	private void setListener(){
		btn_contact_backup.setOnClickListener(clickme);
		btn_contact_recovery.setOnClickListener(clickme);
		imageButton_back.setOnClickListener(clickme);
	}
	
	public OnClickListener clickme = new OnClickListener() {
		@Override
		public void onClick(View v) {
			switch (v.getId()) {
			case R.id.contact_backup_btn:
				startDialog_Backup();
				System.out.println("contact_backup_btn   is  clicked");
				break;
			case R.id.contact_recovery_btn:
				startDialog_Recovery();
				System.out.println("contact_recovery_btn   is  clicked");
				break;
			case R.id.contact_selected_back_ImageButton:
				t.onBackPressed();
				break;
			default:
				break;
			}
		}
	};
	
	
	
	/**
	 * 启动BackUpTask 启动相对应Dialog
	 */
	@SuppressWarnings("static-access")
	public void startDialog_Backup(){
		backup_dialog = new ProgressBackupDialog(t.instance,R.style.Contact_Dialog);
		backup_dialog.setContentView(R.layout.progressdialog_backup);
		backup_dialog.show();
		t.addDialogtoList(backup_dialog);
	}
	/**
	 * 启动RecoveryTask 启动相对应Dialog
	 */
	@SuppressWarnings("static-access")
	public void startDialog_Recovery(){
		recovery_dialog = new ProgressRecoveryDialog(t.instance, R.style.Contact_Dialog);
		recovery_dialog.setContentView(R.layout.progressdialog_recovery);
		recovery_dialog.show();
		t.addDialogtoList(recovery_dialog);
	}
	/**
	 * 获取联系人数目
	 */
	public /*static*/ int countContact(Context context) {
		int count = 0;
		Cursor contactsCursor = null;
		String[] selectCol = new String[]{  
		        ContactsContract.Contacts.DISPLAY_NAME,  
		        ContactsContract.Contacts.HAS_PHONE_NUMBER,  
		        ContactsContract.Contacts._ID  
		    };  
		String RAW_SELECTION_STRING = "((" + Contacts.DISPLAY_NAME + " NOTNULL) AND ("  
			       + Contacts.HAS_PHONE_NUMBER + "=1) AND ("  
			       + Contacts.DISPLAY_NAME + " != '' ))";  
		try {
			contactsCursor = context.getContentResolver().query(  
		            ContactsContract.Contacts.CONTENT_URI, selectCol, RAW_SELECTION_STRING, null,   
		            ContactsContract.Contacts.DISPLAY_NAME + " COLLATE LOCALIZED ASC");
			if (contactsCursor != null) {
				count = contactsCursor.getCount();
			}
			/*while(contactsCursor.moveToNext()){  
				 System.out.println("遍历剔除联系人");
                //遍历所有的联系人下面所有的电话号码  
                String phoneName = contactsCursor.getString(0);  
                String phoneName1 = contactsCursor.getString(1); 
                String phoneName2 = contactsCursor.getString(2); 
                if(phoneName != null)
               	 System.out.println(phoneName  + "  ::phoneName");
                else
               	 System.out.println("  ::phoneName   null");
                if(phoneName1 != null)
               	 System.out.println(phoneName1  + "  ::phoneName1");
                else
               	 System.out.println("  ::phoneName1   null");
                if(phoneName2 != null)
               	 System.out.println(phoneName2  + "  ::phoneName2");
                else
               	 System.out.println("  ::phoneName2   null");
            }*/
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		} finally {
			if (contactsCursor != null) {
				contactsCursor.close();
				contactsCursor = null;
			}
		}
		return count;
	}

}
