---
title: Spring 事务笔记：从代理到提交
date: 2026-10-17
tags: Java, Spring
sample: true
---
这是一篇用于展示博客排版的示例文章，尚未作为正式文章发布。

## 从一个方法调用开始
理解 Spring 事务，可以先沿着一次方法调用往下走：代理拦截调用，事务管理器准备事务，业务方法执行，最后提交或回滚。

> 事务边界不仅由注解决定，也取决于调用是否经过了代理。

## 一个简单的例子
下面的代码展示了常见的声明式事务写法。

```java
@Transactional(rollbackFor = Exception.class)
public void createOrder(Order order) {
    orderRepository.save(order);
    inventoryService.reserve(order.getItems());
}
```

`@Transactional` 为经过代理的方法调用声明事务语义。实际是否开启新事务，还取决于传播行为和当前是否已有事务。

## REQUIRED 与 REQUIRES_NEW
- REQUIRED：有现成的事务就参与，没有则新建。
- REQUIRES_NEW：挂起现有事务，开启独立事务。
- NESTED：在支持的事务管理器下，通常通过保存点建立嵌套边界。

## 我会如何继续学习
把抽象和具体实现分开看：先理解事务管理器的提交、回滚和清理流程，再追踪 JDBC 连接何时获取、何时绑定到当前线程，以及何时释放。

这篇示例可以直接替换为你的第一篇正式笔记。
