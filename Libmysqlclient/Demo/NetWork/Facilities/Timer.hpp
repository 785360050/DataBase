#pragma once

#include <time.h>

#include <arpa/inet.h>

#include <iostream>

#include "Socket.hpp"

#include "Client_Data.hpp"

// const int BUFFER_SIZE = 64;

class Client_Data;

class Timer
{
    // private:
public:
    Timer() = default;
    ~Timer() = default;

public:
    time_t event_timeout;            /// 超时事件(绝对事件)
    void (*function)(Client_Data* user_data); /// 回调函数
    Client_Data *data;               // 回调函数需要处理的数据
public:
    Timer *pre;  // 前节点
    Timer *next; // 后节点
};



// 定时器链表，双向升序，带头结点和尾部节点
class Timer_List
{
private:
    Timer *head;      // 首元结点
    Timer *tail;      // 尾元节点

private:
    void add_timer(Timer *timer, Timer *lst_head)
    {
        Timer *prev = lst_head;
        Timer *tmp = prev->next;
        while (tmp)
        {
            if (timer->event_timeout < tmp->event_timeout)
            {
                prev->next = timer;
                timer->next = tmp;
                tmp->pre = timer;
                timer->pre = prev;
                break;
            }
            prev = tmp;
            tmp = tmp->next;
        }
        if (!tmp)
        {
            prev->next = timer;
            timer->pre = prev;
            timer->next = NULL;
            tail = timer;
        }
    }

public:
    Timer_List() : head(NULL), tail(NULL) {}
    ~Timer_List()
    { // 同步销毁所有定时器
        Timer *tmp = head;
        while (tmp)
        {
            head = tmp->next;
            delete tmp;
            tmp = head;
        }
    }
    // 添加定时器timer
    void Timer_Add(Timer *timer)
    {
        if (!timer)
            return;

        if (!head)
        {
            head = tail = timer;
            return;
        }
        // 根据定时器的超时时间比较(绝对时间)
        if (timer->event_timeout < head->event_timeout)
        { // 插到前面
            timer->next = head;
            head->pre = timer;
            head = timer;
            return;
        }
        // 使用递归找到对应位置插入
        add_timer(timer, head);
    }
    // 定时器变化时，调整该定时器的位置(仅考虑延长时间，向后移动的情况)
    void Timer_Adjest(Timer *timer)
    {
        if (!timer)
            return;
        Timer *tmp = timer->next;
        if (!tmp || (timer->event_timeout < tmp->event_timeout)) // 当前在尾节点，或延长时间后不需要移动
            return;

        if (timer == head)
        { // 若当前定时器为首元素,则删除当前定时器，重新添加到合适位置
            head = head->next;
            head->pre = NULL;
            timer->next = NULL;
            add_timer(timer, head);
        }
        else
        { // 否则移动到合适位置
            timer->pre->next = timer->next;
            timer->next->pre = timer->pre;
            add_timer(timer, timer->next);
        }
    }
    // 删除定时器timer
    void Timer_Delete(Timer *timer)
    {
        if (!timer)
            return;
        if ((timer == head) && (timer == tail)) // 仅一个元素
        {
            delete timer;
            head = NULL;
            tail = NULL;
            return;
        }
        if (timer == head) // 多个元素，且为首元素
        {
            head = head->next;
            head->pre = NULL;
            delete timer;
            return;
        }
        if (timer == tail) // 多个元素，且为尾元素
        {
            tail = tail->pre;
            tail->next = NULL;
            delete timer;
            return;
        }
        timer->pre->next = timer->next;
        timer->next->pre = timer->pre;
        delete timer;
    }
    // 核心心搏函数，定时执行，检查到期的任务
    // 添加定时器O(n),删除定时器O(1),执行定时器O(1)
    void Tick()
    {
        if (!head)
            return;
        std::cout << "Timer Ticked" << std::endl;
        time_t cur = time(NULL);
        Timer *tmp = head;
        while (tmp)
        {
            if (cur < tmp->event_timeout)
                break;
            tmp->function(tmp->data); // 回调

            // 删除定时器
            head = tmp->next;
            if (head)
                head->pre = NULL;
            delete tmp;
            tmp = head;
        }
    }
};