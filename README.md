# gurulab-erp

```sql
                +---------------+
                |   Web / API   |
                +-------+-------+
                        |
                +-------v--------+       +------------+
                | EventHandler   |       | EventModule |
                +-------+--------+       +------+------+
                        |                      ^
        +---------------+-----+----------------+----+
        |               |     |                     |
+-------v-------+ +-----v-----+     +-----v-------+ +-------v---------+
|TicketController| |UserController| |LoggerModule  | |ScheduledTasks  |
+-------+-------+ +-----+-----+     +-----+-------+ +-------+---------+
        |               |                 |                 |
        |               |                 |                 |
+-------v-------+ +-----v-----+     +-----v-------+         |
|  Ticket DB    | |  User DB  |     |  Logger DB  |<--------+
+-------+-------+ +-----+-----+     +-----+-------+
        |               |                 |
        |               |                 |
+-------v-------+ +-----v-----+     +-----v-------+
| Ticket Module | |User Module|     |Logger Module|
+---------------+ +-----------+     +-------------+

```

## Ticket
```doctest
Ticket is the core element of the ERP system.
Every ticket is a node of a tree structure (a workflow). If a ticket has no upstream_ticket, 
it is the head of the tree. 
A dummy ticket has no sub_tickets and no 'next tickets', like a single item of
 a todo list.
In most cases, a ticket is a todo-list. We use the concept of a 
sub-ticket to implement the todo-list.
In some cases, the life-cycle of a ticket is more complicated. So we need the 
.next method to describe the tickets pathway.

ticket_id: unique id
ticket_type: ticket type
ticket_name: ticket name
source: 工单来源 0-system 1-user
upstream_ticket: None if not a subticket
assign_method: user_group_random/user_assign
assigned_to: User
timestamp: datetime类型

deadline: the expected time for the ticket to be completed (datetime类型)
state: open/closed/finished


Ticket.sub_tickets: return a list of sub-tickets which should be automatically generated 
simultaneously with the ticket, the sub-tickets are parallel.

Ticket.next: return a list of tickets which should be generated after this 
ticket is closed or finished. 
 
Ticket.todo_list: 遍历全部的Ticket.sub and Ticket.next，返回所有子工单列表

Ticket.json: 将ticket序列化，返回dict，用于mongodb存储

```
Ticket是一个抽象类，而Ticket.sub/Ticket.next/Ticket.assign是抽象方法（接口）需要由子类来继承实现。

## User
```doctest
username
password_hash
roles
```

## Controller
```doctest
Controller is used to manipulate tickets, communicate with databases. It is event-driven.
```