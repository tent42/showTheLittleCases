#include <iostream>
#include <windows.h>
#include <string>
using namespace std;

struct NODE 
{
    unsigned long uID;
    string str;
    NODE *next;
};

class cList
{
public:
    cList(int n);
    ~cList() {}
    bool iscreated(); //�����Ƿ񴴽��ɹ�
    int showNodeCount() const; //��������Ľڵ���
    void printList() const; //�����������ÿһ�ڵ������
    void addNodeBefore(unsigned long uID); //��ָ���ڵ�ǰ����һ���µĽڵ�
    void addNodeAfter(unsigned long uID); //��ָ���ڵ�����һ���µĽڵ�
    void deleteNode(unsigned long uID); //ɾ��ָ���Ľڵ�
    void sortList(); //����ID��С�����������������
protected:
private:
    int nCount; //����ڵ���
    NODE *pHead; //�����׽ڵ�ָ��
    NODE *pDest, *pFront;

    NODE *createNode(int n); //��������
    //void initList(NODE *pDest); //��ʼ���ڵ�����
    void searchNode(unsigned long uID); //����ID�����ID��ȵĵ�һ���ڵ�
};