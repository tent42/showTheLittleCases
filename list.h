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
    bool iscreated(); //链表是否创建成功
    int showNodeCount() const; //返回链表的节点数
    void printList() const; //遍历链表并输出每一节点的数据
    void addNodeBefore(unsigned long uID); //在指定节点前插入一个新的节点
    void addNodeAfter(unsigned long uID); //在指定节点后添加一个新的节点
    void deleteNode(unsigned long uID); //删除指定的节点
    void sortList(); //根据ID大小对链表进行升序排序
protected:
private:
    int nCount; //链表节点数
    NODE *pHead; //链表首节点指针
    NODE *pDest, *pFront;

    NODE *createNode(int n); //创建链表
    //void initList(NODE *pDest); //初始化节点数据
    void searchNode(unsigned long uID); //搜索ID与给定ID相等的第一个节点
};