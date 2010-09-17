Introduction
============

It should be easy to make a FormFolder (ActionLetter) store its data in MySQL.
This product aims to facilitate storing data from PloneFormGen (and also
collective.megaphone) in a MySQL database.  
(It may later work for other SQL dialects also, hence the name
Products.sqlpfgadapter.)

You could also save PFG data in SQL by using a Z SQL Method as an
after-validation script.
(http://plone.org/products/ploneformgen/documentation/tutorial/sql-crud) 
This works as well, but: 

- it's quite cumbersome for ordinary users
- it doesn't work with collective.megaphone 
  (http://plone.293351.n2.nabble.com/plan-for-easy-MySQL-storage-for-collective-megaphone-td5481845.html#a5481845).

The goal for this package is:

- to be easy to use for ordinary people
- to work with collective.megaphone

Approach
========

We create a new PloneFormGen Action Adapter. 
This uses SQLAlchemy (collective.lead) to save the form data to the database.


Installing
==========

Developers
----------

To install a complete development setup::

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

    A database table will be created. Its name is generated (from the Form
    Folder's id, among others), you can see it by viewing the adapter object.
    The table has an 'id' column, and a column for each form field.

That's it! From now on, succesfully submitted forms will be stored in the
database.

Usage with collective.megaphone
-------------------------------

Not implemented yet.


Limitations
===========

This product is under development. For now, we have major limitations:

- Not all PloneFormGen fields work, notably:

  - file field
  - decimal field
  - rating-scale field

- Adding and removing fields, or changing their names, doesn't change the
  database table. Field names for which there is no column will just be
  discarded.


To do
=====

* Test collective.megaphone compatibility
* Support all form field types.
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
