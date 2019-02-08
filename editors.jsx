import 'selfAsset/css/braftmain.css';
import React from 'react';
import { connect } from 'react-redux';
import { constant as editorConstant } from '../store';
import { Form, Input, Button, Radio, Tooltip, Icon, Modal, message } from 'antd';
import BraftEditor from 'braft-editor';
import * as clientHelper from './../../../../../tools/clientHelper';
import * as clientLocalStorage from './../../../../../tools/clientLocalStorage';
import { Helmet } from 'react-helmet';
import createBrowserHistory from 'history/createBrowserHistory';
import config from 'selfConfig';
const FormItem = Form.Item;
const confirm = Modal.confirm;
class Editors extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      outputHTML: '<p></p>',
      state_category: ''
    };
  }
  uploadFunc = (param) => {
    if (param.file.size > config.defaultMediaSize) {
      message.error(`上传的文件需要小于${config.defaultMediaSize / 1024}kb`);
      param.error({
        msg: '上传的文件过大❎'
      });
      return null;
    }
    clientHelper
      .compressImage(URL.createObjectURL(param.file) /**, 400, 400 */)
      .then((result) => {
        param.success({
          url: result.url,
          width: result.width,
          height: result.height
        });
      })
      .catch((error) => {
        param.error();
      });
  };

  showConfirm = (vthis, values) => {
    confirm({
      title: '确认提交',
      content: (
        <p>
          确认要<span style={{ color: 'red' }}>提交</span>当前内容吗？
          <br />
          点击<span style={{ color: 'red' }}>提交</span>成功后，页面将跳转入编辑前页面
          <br />
          如果想继续编辑可点击<span style={{ color: 'red' }}>取消</span>按钮
        </p>
      ),
      okText: '提交',
      cancelText: '取消',
      onOk() {
        const checklistcontent = values.content.toRAW(true);
        values.content = JSON.stringify(values.content.toRAW(true));
        values.listcontent = '';
        for (let index = 0; index < checklistcontent.blocks.length; index++) {
          values.listcontent += checklistcontent.blocks[index].text;
        }
        if (values.listcontent.length > 9) {
          if (
            !clientHelper.isNull(checklistcontent.entityMap[0]) &&
            !clientHelper.isNull(checklistcontent.entityMap[0].data)
          ) {
            clientHelper
              .compressImage(
                JSON.stringify(checklistcontent.entityMap[0].data.url).replace(/^"|"$/g, ''),
                272,
                272,
                0.85
              )
              .then((result) => {
                values.listimg = result.url.replace(/^"|"$/g, '');
                vthis.props.handleSubmitData(values);
              })
              .catch((error) => {
                param.error();
              });
          } else {
            values.listimg = '';
            vthis.props.handleSubmitData(values);
          }
        } else {
          vthis.props.EditorshowInfo('正文中需要最少10个文字描述');
        }
      },
      onCancel() {}
    });
  };

  componentDidMount() {
    const res = clientLocalStorage.getLocalStorage('content');
    let defaultEditorState;
    for (var v of res) {
      if (!clientHelper.isNull(v)) {
        defaultEditorState = v;
      }
    }
    if (clientHelper.isNull(this.props.defaultEditorState)) {
      if (!clientHelper.isNull(defaultEditorState)) {
        defaultEditorState = BraftEditor.createEditorState(defaultEditorState);
        this.props.setDefaultEditorState(defaultEditorState);
      }
    }
    this.props.needEditorId
      ? this.props.getInitEditorData(this.props.needEditorId, this.props.needEditorTabs)
      : null;
    this.props.onLoaded();
    this.props.getInitEditorRadioButtonData();
  }

  handleSubmit = (event) => {
    event.preventDefault();
    this.props.form.validateFields((error, values) => {
      if (!error) {
        this.showConfirm(this, values);
      }
    });
  };
  validateKeywords = (rule, value, callback) => {
    if (value && value.length >= 2) {
      if (value.length > 60) {
        callback('标签间以空格隔开,如标签1 标签2,标签总字数不大于60个字');
      } else {
        callback();
      }
    } else {
      callback('标签间以空格隔开,如标签1 标签2,标签总字数不小于2个字');
    }
  };
  handleEditorChange = (editorState) => {
    const res = clientLocalStorage.getLocalStorage('content');
    let defaultEditorState;
    for (var v of res) {
      if (!clientHelper.isNull(v)) {
        defaultEditorState = v;
      }
    }
    let AutoSaveThreshold = 0;
    if (clientHelper.isNull(defaultEditorState)) {
      AutoSaveThreshold = editorState.toRAW().length;
    } else {
      AutoSaveThreshold = editorState.toRAW().length - defaultEditorState.length;
    }
    if (AutoSaveThreshold > 50 || (AutoSaveThreshold < -50 && editorState.toHTML() > 17)) {
      this.handleEditorAutoSave(editorState);
    }
  };

  handleEditorSave = (editorState) => {
    const editorData = editorState.toRAW();
    this.props.saveEditorData(false, editorData);
  };

  handleEditorAutoSave = (editorState) => {
    const editorData = editorState.toRAW();
    this.props.saveEditorData(true, editorData);
  };

  componentDidUpdate() {
    /**
     * 跳转到上一页面
     */
    if (this.props.isEditorSuccess) {
      if (this.props.inPage) {
        /**
         * @todo 页面内编辑页面
         */
        const history = createBrowserHistory();
        history.goBack();
        /**
         * 清除localstorage
         */
        const iter = clientLocalStorage.deleteLocalStorage();
        while (iter.next().done !== true) {}
        this.props.signUpClose();
      } else {
        /**
         * @todo 弹窗内编辑页面
         */
        /**
         * 清除localstorage
         */
        const iter = clientLocalStorage.deleteLocalStorage();
        while (iter.next().done !== true) {}
        this.props.signUpClose();
        // this.props.closeModels();
        window.location.reload(true);
      }
    }
  }

  render() {
    const { getFieldDecorator } = this.props.form;
    const { inPage, tabsANDcategory, defaultEditorState } = this.props;
    const { state_category } = this.state;
    const styles = inPage
      ? {
        backgroundColor: '#fff',
        boxShadow: '2px 0 8px rgba(0,0,0,0.1)',
        borderRadius: '6px',
        padding: '5px 15px 5px 15px'
      }
      : {};
    return (
      <div style={{ ...styles }}>
        <Helmet>
          <title>写点什么_孤搞之人</title>
        </Helmet>
        <Form onSubmit={this.handleSubmit} className="form-style">
          <FormItem
            label={
              <span>
                文章标题&nbsp;
                <Tooltip title="文章标题最大长度为50个字">
                  <Icon type="question-circle-o" />
                </Tooltip>
              </span>
            }>
            {getFieldDecorator('title', {
              rules: [
                {
                  required: true,
                  message: '请输入标题'
                }
              ]
            })(<Input size="large" placeholder="请输入标题" />)}
          </FormItem>
          <FormItem
            label={
              <span>
                文章栏目&nbsp;
                <Tooltip title="文章栏目必选,选择的哪个栏目,文章就会出现在哪个位置">
                  <Icon type="question-circle-o" />
                </Tooltip>
              </span>
            }>
            {getFieldDecorator('tabs', {
              rules: [
                {
                  required: true,
                  message: '请选择文章栏目'
                }
              ]
            })(
              <Radio.Group onChange={this.wenZhangLanMuChanged} /**defaultValue="horizontal"  */>
                {tabsANDcategory ? (
                  tabsANDcategory.map((item, index) => {
                    return (
                      <Radio.Button key={index} value={item.tabs}>
                        {item.tabs}
                      </Radio.Button>
                    );
                  })
                ) : (
                  <Radio.Button value="horizontal">载入中,或许需要刷新一下...</Radio.Button>
                )}
              </Radio.Group>
            )}
          </FormItem>
          <FormItem
            label={
              <span>
                文章分类&nbsp;
                <Tooltip title="文章分类只是对文章进行归纳,以及一些细节不同,不影响大的方面">
                  <Icon type="question-circle-o" />
                </Tooltip>
              </span>
            }>
            {getFieldDecorator('category', {
              rules: [
                {
                  required: true,
                  message: '请选择文章分类'
                }
              ]
            })(
              <Radio.Group /**defaultValue="horizontal"  onChange={this.handleFormLayoutChange}*/>
                {state_category ? (
                  state_category.map((item, index) => {
                    return (
                      <Radio.Button key={index} value={item}>
                        {item}
                      </Radio.Button>
                    );
                  })
                ) : (
                  <Radio.Button value="0">请先选择文章栏目...</Radio.Button>
                )}
              </Radio.Group>
            )}
          </FormItem>
          <FormItem
            label={
              <span>
                文章标签&nbsp;
                <Tooltip title="请输入正确的文章标签:标签间以空格隔开,如标签1 标签2,标签总字数不小于2个字,不大于60个字">
                  <Icon type="question-circle-o" />
                </Tooltip>
              </span>
            }>
            {getFieldDecorator('keywords', {
              rules: [
                {
                  required: true,
                  message:
                    '请输入正确的文章标签:标签间以空格隔开,如标签1 标签2,标签总字数不小于2个字,不大于60个字'
                },
                {
                  validator: this.validateKeywords
                }
              ]
            })(<Input size="large" placeholder="请输入标题" />)}
          </FormItem>
          <FormItem
            label={
              <span>
                文章正文&nbsp;
                <Tooltip
                  title="
                  可以通过快捷键Crtl+S(Windows)或⌘+S(Mac)进行快速保存。
                  文章正文编辑已经提供了自动保存的功能，当意外退出时，下次再次进入编辑页面，会还原上次编辑内容。
                  但只提供对当前正文的自动保存，当前文章在提交后自动保存内容也将消失。
                  其他如文章标题等不会保存。而且请注意，如果文章内容过大（可注意网站中上方的信息回馈）时，
                  便不再自动保存，而是等待最后的文章提交。">
                  <Icon type="question-circle-o" />
                </Tooltip>
              </span>
            }>
            {getFieldDecorator('content', {
              validateTrigger: 'onBlur',
              rules: [
                {
                  required: true,
                  validator: (_, value, callback) => {
                    if (value.isEmpty()) {
                      callback('请输入正文内容');
                    } else {
                      callback();
                    }
                  }
                }
              ]
            })(
              defaultEditorState ? (
                <BraftEditor
                  onChange={this.handleEditorChange}
                  onSave={this.handleEditorSave}
                  media={{ uploadFn: this.uploadFunc }}
                  className="my-editor"
                  placeholder="可以通过快捷键Crtl+S(Windows)或⌘+S(Mac)进行快速保存。&#10;请输入正文内容&#10;媒体大小请选择大小为500kb以下&#10;如果需要更大的视频展示,请选择媒体库下的{添加网络资源按钮进行添加}&#10;"
                  defaultValue={defaultEditorState}
                  // initialValue={defaultEditorState}
                />
              ) : (
                <BraftEditor
                  onChange={this.handleEditorChange}
                  onSave={this.handleEditorSave}
                  media={{ uploadFn: this.uploadFunc }}
                  className="my-editor"
                  placeholder="可以通过快捷键Crtl+S(Windows)或⌘+S(Mac)进行快速保存。&#10;请输入正文内容&#10;图片大小请选择500KB一下的图片大小&#10;目前暂不支持视频上传,如果需要视频展示,请选择媒体库下的{添加网络资源按钮进行添加}&#10;"
                />
              )
            )}
          </FormItem>
          <FormItem>
            <Button size="large" type="primary" htmlType="submit">
              提交
            </Button>
          </FormItem>
        </Form>
      </div>
    );
  }
  wenZhangLanMuChanged = (event) => {
    for (let i = 0; i < this.props.tabsANDcategory.length; i++) {
      if (event.target.value === this.props.tabsANDcategory[i].tabs) {
        this.setState({
          state_category: this.props.tabsANDcategory[i].category
        });
      }
    }
  };
}

const mapStateToProps = (state) => {
  return {
    tabsANDcategory: state.editor.tabsANDcategory,
    defaultEditorState: state.editor.defaultEditorState,
    isEditorSuccess: state.editor.isEditorSuccess
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    onLoaded() {
      dispatch({
        type: 'loaded'
      });
    },
    getInitEditorData(id, tabs) {
      dispatch({
        type: editorConstant.getInitEditorData,
        payload: {
          id,
          tabs
        }
      });
    },
    getInitEditorRadioButtonData() {
      dispatch({
        type: editorConstant.getInitEditorRadioButtonData
      });
    },
    saveEditorData(autosave, editorData) {
      dispatch({
        type: editorConstant.saveEditorData,
        payload: {
          autosave,
          editorData
        }
      });
    },
    handleSubmitData(value) {
      dispatch({
        type: editorConstant.handleSubmitData,
        payload: {
          title: value.title,
          tabs: value.tabs,
          category: value.category,
          keywords: value.keywords,
          content: value.content,
          listcontent: value.listcontent,
          listimg: value.listimg
        }
      });
    },
    setDefaultEditorState(defaultEditorState) {
      dispatch({
        type: editorConstant.setDefaultEditorState,
        payload: {
          defaultEditorState
        }
      });
    },
    EditorshowInfo(messaga) {
      dispatch({
        type: editorConstant.EditorshowInfo,
        payload: {
          messaga
        }
      });
    },
    signUpClose() {
      dispatch({
        type: editorConstant.isEditorSuccessReducer,
        payload: {
          isEditorSuccess: false
        }
      });
    }
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Form.create()(Editors));
