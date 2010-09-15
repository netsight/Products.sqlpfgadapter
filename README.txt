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

If you use another buildout configuration, see dependencies below.

After running buildout, collective.recipe.plonesite should have created a Plone
site with id 'Plone', and with PloneFormGen, plone.app.registry and this
product installed.


Configuration
=============

As a site admin, go to the "SQL Settings" in Plone's control panel. You'll be
taken to "@@sqlpfg-controlpanel". Here you can set your database connection
settings.


Usage
=====

To save a form's data in the database, add a "MySQL Adapter" from the "Add
new..." menu in the Form Folder. Give it a title and save it.

A database table will be created. Its name is taken from the Form Folder's id
(you can see it by viewing the adapter object.) The table has an 'id' column,
and a column for each form field.

From now on, succesfully submitted forms will be stored in the database!

Usage with collective.megaphone
-------------------------------

Not implemented yet.


Limitations
===========

This product is under development, so for now we have severe limitations:

- You can only use form fields of the type "String" (type_name
  FormStringField).

- Adding and removing fields, or changing their names, doesn't change the
  database table. Field names for which there is no column will just be
  discarded.


To do
=====

 * Test collective.megaphone compatibility
 * Create different column types for different form field types. Currently only
   string fields are supported;
 * Test Plone 4 compatibility;
 * Allow updating tables when fields are added;


Compatibility / Dependencies
============================

Tested on Plone 3.3.5

This product uses plone.app.registry for its controlpanel. In order for it to
work, add this to your buildout::

    [buildout]
    extends +=
        http://good-py.appspot.com/release/plone.app.registry/1.0b2?plone=3.3.5

    [versions]
    z3c.form = 1.9.0
