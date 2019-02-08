#include "list.h"
#include "stdlib.h"  //���������malloc�������������ڴ�����XXsize�ռ�ĺ�����
#include "assert.h"

cList::cList(int n)
{
    nCount = n;
    pHead = createNode(n);
}

//��������
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

//��ʼ���ڵ�����
//void cList::initList(NODE *pDest)
//{
//    assert(pDest != NULL);
//    cout<<"�������½��ڵ�� ID �� ���ƣ�"<<endl;
//    cin>>pDest->uID>>pDest->str;
//}

//�����Ƿ񴴽��ɹ�
bool cList::iscreated()
{
    if (pHead != NULL)
    {
        return true;
    }
    return false;
}

//��������Ľڵ���
int cList::showNodeCount() const
{
    return nCount;
}

//�����������ÿһ�ڵ������
void cList::printList() const
{
    NODE *pTemp = pHead;
    while (pTemp != NULL)
    {
        cout<<pTemp->uID<<" "<<pTemp->str<<endl;
        pTemp = pTemp->next;
    }
}

//����ID�����ID��ȵĵ�һ���ڵ�
void cList::searchNode(unsigned long uID)
{
    pDest = pHead;
    while ((pDest != NULL) && (pDest->uID != uID))
    {
        pFront = pDest;
        pDest = pDest->next;
    }
}

////��ָ���ڵ�ǰ����һ���µĽڵ�
//void cList::addNodeBefore(unsigned long uID)
//{
//    NODE *pNewNode;
//    searchNode(uID);
//    if (pDest == NULL)
//    {
//        cout<<"δ�ҵ�ָ���ڵ㣡"<<endl;
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
////��ָ���ڵ�����һ���µĽڵ�
//void cList::addNodeAfter(unsigned long uID)
//{
//    NODE *pNewNode;
//    searchNode(uID);
//    if (pDest == NULL)
//    {
//        cout<<"δ�ҵ�ָ���ڵ㣡"<<endl;
//        return;
//    }
//    pNewNode = new NODE;
//    initList(pNewNode);
//    pNewNode->next = pDest->next;
//    pDest->next = pNewNode;
//    pDest = NULL;
//    nCount++;
//}

//ɾ��ָ���Ľڵ�
void cList::deleteNode(unsigned long uID)
{
    searchNode(uID);
    if (pDest == NULL)
    {
        cout<<"δ�ҵ�ָ���ڵ㣡"<<endl;
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

//����ID��С�����������������ð�����򷨣�
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