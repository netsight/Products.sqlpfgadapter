Introduction
============

The goal for this package is:

- to make SQL storage from PloneFormGen easy
- to be usable with collective.megaphone

To achieve this, we create a new PloneFormGen action-adapter_. 
This uses SQLAlchemy_ (collective.lead_) to save the form data to the database.
(SQLAlchemy should work on most SQL dialects.)

You could also save PFG data in SQL by using a Z SQL Method as an
after-validation script, as described in the SQL-CRUD-tutorial_.  
This works, but: 

- it's a lot of manual work, and quite cumbersome for ordinary users
- it doesn't work with collective.megaphone_ (see mailinglist-discussion_)


Installing
==========

Developers
----------

To install a complete development setup::

    svn co https://svn.plone.org/svn/collective/Products.PloneFormGen/adapters/Products.sqlpfgadapter/buildout/plone4 sqlpfg-plone4
    cd sqlpfg-plone4
    python2.6 bootstrap.py
    ./bin/buildout -c buildout-dvl.cfg

Or, for Plone 3:

    svn co https://svn.plone.org/svn/collective/Products.PloneFormGen/adapters/Products.sqlpfgadapter/buildout/plone3 sqlpfg-plone3
    cd sqlpfg-plone3
    python2.4 bootstrap.py
    ./bin/buildout -c buildout-dvl.cfg

If you use another buildout configuration, be sure to include the "Known good
set" for plone.app.registry for your version of Plone.

    [versions]
    z3c.form = 1.9.0

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

To save a form's data in the database, add an "SQL Storage" from the "Add
new..." menu in the Form Folder. Give it a title and save it.

    A database table will be created. Its name is generated (from the Form
    Folder's id, among others), you can see it by viewing the adapter object.
    The table has an 'id' column, and a column for each form field.

That's it! From now on, succesfully submitted forms will be stored in the
database.

Usage with collective.megaphone
-------------------------------

The product will work just as well with collective.megaphone. However, to be
able to add the action adapter to an Action Letter or Megaphone Action, you
have to add "SQLPFGAdapter" to the "Allowed content types" via the ZMI.

The product collective.megaphonesql_ can do this for you.


Limitations
===========

This product is under development. For now, we have major limitations:

- Not all PloneFormGen fields work, notably:

  - file field
  - rating-scale field

- Adding and removing fields, or changing their names, doesn't change the
  database table. Field names for which there is no column will just be
  discarded.


Compatibility / Dependencies
============================

Tested with: 

- Plone: 3.3.5, 4.0 
- PloneFormGen: 1.6.0b4, 1.6.0b5
- megaphone: 1.4.1, 2.0b1
- collective.lead 1.0, SQLAlchemy 0.4.8
- SQL: MySQL 5.1.41

This product uses plone.app.registry for its controlpanel. In order for it to
work, use its "Known good set" (see section "Developers" above).

.. _PloneFormGen: http://plone.org/products/ploneformgen
.. _collective.megaphone: http://plone.org/products/megaphone
.. _SQL-CRUD-tutorial: http://plone.org/products/ploneformgen/documentation/tutorial/sql-crud 
.. _mailinglist-discussion: http://plone.293351.n2.nabble.com/plan-for-easy-MySQL-storage-for-collective-megaphone-td5481845.html#a5481845
.. _action-adapter: http://plone.org/products/ploneformgen/documentation/reference/fields-and-objects/adapters
.. _SQLAlchemy: http://www.sqlalchemy.org
.. _collective.lead: http://pypi.python.org/pypi/collective.lead
..  _collective.megaphonesql: http://svn.plone.org/svn/collective/collective.megaphonesql 
