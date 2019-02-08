#include "list.h"
#include "stdlib.h"  //里面包含了malloc函数，可以像内存申请XXsize空间的函数。
#include "assert.h"

cList::cList(int n)
{
    nCount = n;
    pHead = createNode(n);
}

//创建链表
//NODE *cList::createNode(int n)
//{
//    NODE *pHead, *pRear, *pNewNode;
//    int i;
//    for (i=0; i<n; i++)
//    {
//        pNewNode = new NODE;
//        initList(pNewNode);
//        if (0==i)
//        {
//            pRear = pHead = pNewNode;
//        } 
//        else
//        {
//            pRear->next = pNewNode;
//        }
//        pNewNode->next = NULL;
//        pRear = pNewNode;
//    }
//    return pHead;
//}

//初始化节点数据
//void cList::initList(NODE *pDest)
//{
//    assert(pDest != NULL);
//    cout<<"请输入新建节点的 ID 和 名称："<<endl;
//    cin>>pDest->uID>>pDest->str;
//}

//链表是否创建成功
bool cList::iscreated()
{
    if (pHead != NULL)
    {
        return true;
    }
    return false;
}

//返回链表的节点数
int cList::showNodeCount() const
{
    return nCount;
}

//遍历链表并输出每一节点的数据
void cList::printList() const
{
    NODE *pTemp = pHead;
    while (pTemp != NULL)
    {
        cout<<pTemp->uID<<" "<<pTemp->str<<endl;
        pTemp = pTemp->next;
    }
}

//搜索ID与给定ID相等的第一个节点
void cList::searchNode(unsigned long uID)
{
    pDest = pHead;
    while ((pDest != NULL) && (pDest->uID != uID))
    {
        pFront = pDest;
        pDest = pDest->next;
    }
}

////在指定节点前插入一个新的节点
//void cList::addNodeBefore(unsigned long uID)
//{
//    NODE *pNewNode;
//    searchNode(uID);
//    if (pDest == NULL)
//    {
//        cout<<"未找到指定节点！"<<endl;
//        return;
//    }
//    pNewNode = new NODE;
//    initList(pNewNode);
//    if (pDest == pHead)
//    {
//        pNewNode->next = pHead;
//        pHead = pNewNode;
//    }
//    else
//    {
//        pNewNode->next = pDest;
//        pFront->next = pNewNode;
//    }
//    pDest = NULL;
//    pFront = NULL;
//    nCount++;
//}
//
////在指定节点后添加一个新的节点
//void cList::addNodeAfter(unsigned long uID)
//{
//    NODE *pNewNode;
//    searchNode(uID);
//    if (pDest == NULL)
//    {
//        cout<<"未找到指定节点！"<<endl;
//        return;
//    }
//    pNewNode = new NODE;
//    initList(pNewNode);
//    pNewNode->next = pDest->next;
//    pDest->next = pNewNode;
//    pDest = NULL;
//    nCount++;
//}

//删除指定的节点
void cList::deleteNode(unsigned long uID)
{
    searchNode(uID);
    if (pDest == NULL)
    {
        cout<<"未找到指定节点！"<<endl;
        return;
    }
    if (pDest == pHead)
    {
        pHead = pHead->next;
    } 
    else
    {
        pFront->next = pDest->next;
    }
    pDest = NULL;
    pFront = NULL;
    delete pDest;
    nCount--;
}

//根据ID大小对链表进行升序排序（冒泡排序法）
void cList::sortList()
{
    int i;
    for (i=0; i<nCount-1; i++)
    {
        pDest = pHead;
        while (pDest->next != NULL)
        {
            if (pDest == pHead)
            {
                if (pDest->uID > pDest->next->uID)
                {
                    pHead = pDest->next;
                    pDest->next = pHead->next;
                    pHead->next = pDest;
                    pFront = pHead;
                } 
                else
                {
                    pFront = pDest;
                    pDest = pDest->next;
                }
            } 
            else
            {
                if (pDest->uID > pDest->next->uID)
                {
                    pFront->next = pDest->next;
                    pDest->next = pDest->next->next;
                    pFront->next->next = pDest;
                    pFront = pFront->next;
                } 
                else
                {
                    pFront = pDest;
                    pDest = pDest->next;
                }
            }
        }
    }
    pFront = NULL;
    pDest = NULL;
} ;