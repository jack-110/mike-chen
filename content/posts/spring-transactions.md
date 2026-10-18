---
title: Spring Transactions: From Proxy to Commit
date: 2026-10-17
category: Tech
tags: Spring
sample: true
---
This sample post demonstrates the blog’s layout. It is not a formally published technical article.

## Start with a method call
To understand Spring transactions, follow a single method call: a proxy intercepts the call, a transaction manager prepares the transaction, the business method runs, and the transaction is committed or rolled back.

> A transaction boundary depends on whether the call passes through a proxy, as well as on the annotation.

## A simple example
Here is a typical use of declarative transaction management.

```java
@Transactional(rollbackFor = Exception.class)
public void createOrder(Order order) {
    orderRepository.save(order);
    inventoryService.reserve(order.getItems());
}
```

`@Transactional` declares transaction semantics for a method invocation intercepted by the proxy. Whether a new transaction is started also depends on the propagation behavior and any existing transaction.

## REQUIRED and REQUIRES_NEW
- REQUIRED: participate in an existing transaction, or start a new one if none exists.
- REQUIRES_NEW: suspend the existing transaction and start an independent one.
- NESTED: with a supporting transaction manager, typically use a savepoint to establish a nested boundary.

## Where I would look next
Separate the abstraction from its implementation. First follow the transaction manager’s commit, rollback, and cleanup paths. Then trace when a JDBC connection is acquired, bound to the current thread, and released.

Replace this sample with your first real note whenever you are ready.
