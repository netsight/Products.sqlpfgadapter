Introduction
============

It should be easy to make a FormFolder (ActionLetter) store its data in MySQL.
This product aims to facilitate storing data from PloneFormGen, and more
importantly collective.megaphone, in a MySQL database.
(It may later work for other SQL dialects also, hence the name
Products.sqlpfgadapter.)

It is created for the purpose of using with collective.megaphone. Currently,
overriding the after-validation script with a Z MySQL Method (as recommended in
http://plone.org/products/ploneformgen/documentation/tutorial/sql-crud) isn't user friendly enough. More important, it doesn't
work with c.m because that sets its own after-validation script
(@@recipient_multiplexer). (See discussion at
http://plone.293351.n2.nabble.com/plan-for-easy-MySQL-storage-for-collective-megaphone-td5481845.html#a5481845)


Approach
========

We create a new PloneFormGen Action Adapter. This may either call a Z MySQL
Method from its onSuccess method, or address MySQL in a more direct way.


To do
=====

 * Get it working with manually created Z MySQL Method
 * Then either:
   - Call the Z MySQL connection directly, or
   - Create the Z MySQL Method on the fly
 * Global controlpanel settings for DB location, user, password
 * Plone 4 compatibility (deprecation messages from ZMySQLDA)


Compatibility / Dependencies
============================

Tested on Plone 3.3.5
