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

We create a new PloneFormGen Action Adapter. 
This uses collective.lead to save the form data to the database.


Installing
==========

This is currently only possible in a development setup, as there is no egg
released yet::

    svn co https://svn.plone.org/svn/collective/Products.PloneFormGen/adapters/Products.sqlpfgadapter/buildout/plone3 sqlpfg-plone3
    cd sqlpfg-plone3
    python2.4 bootstrap.py
    ./bin/buildout -c buildout-dvl.cfg

If you use another buildout configuration, remember to use the KGS at http://good-py.appspot.com/release/plone.app.registry/1.0b2?plone=3.3.5


To do
=====

 * Create table and save data
 * Global controlpanel settings for DB location, user, password
 * Test Plone 4 compatibility


Compatibility / Dependencies
============================

Tested on Plone 3.3.5
