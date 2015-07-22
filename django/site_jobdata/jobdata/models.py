from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    )
from django.conf import settings
import django.core.files.base

# Create your models here.

import os
import json
import subprocess

import myjson

import jobdata.funcs

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

#class FileModel(models.Model):

class Person(models.Model):
    user = models.OneToOneField(MyUser)
    file = models.FileField(null=True, blank=True)

    def file_read(self):
        f = self.file
        if f:
            s = f.read()
            #print "file:"
            #print s
        else:
            #print "file not found"
            s = "{}"
        return s
    def file_read_json(self):
        s = self.file_read()
        try:
            j = json.loads(s)
        except Exception as e:
            print repr(s)
            raise e
        return j

    def file_write(self, s):
        fn = jobdata.funcs.clean(self.user.email) + '.json'
        cf = django.core.files.base.ContentFile(s)
        self.file.save(fn, cf)


    def file_write_json(self, j):
        s = json.dumps(j)
        self.file_write(s)
   
    def __unicode__(self):
        return self.user.email

    def validate_json(self):
        j = self.file_read_json()
        
        #for v in jobdata.myjson.json_iter_list_of_dict(j):
        for v in myjson.iter_list_of_dict(j):
            if myjson.list_of_dict_field_any(v, 'version'):
                #print "adding fields"
                myjson.list_of_dict_add_field_if_not_exists(v, 'version', [])
                myjson.list_of_dict_add_field_if_not_exists(v, '_selector', {})
        self.file_write_json(j)


class DocTemplate(models.Model):
    path    = models.CharField(max_length=256)
    def extension(self):
        t,h = os.path.splitext(self.path)
        return h
    def __unicode__(self):
        return self.path

def upload_to_func(self,_):
    print "upload_to_func"
    return self.filename()

class Document(models.Model):
    person    = models.ForeignKey(Person)
    position  = models.ForeignKey('Position', null=True, blank=True)
    template  = models.ForeignKey(DocTemplate)

    options   = models.TextField(max_length=256)

    file      = models.FileField(null=True, blank=True, upload_to=upload_to_func)

    def extension(self):
        return self.template.extension()

    def get_options_json(self):
        options_json = json.loads(self.options)
    
        if not options_json.has_key('version'):
            options_json['version'] = []
    
        if not options_json.has_key('order'):
            options_json['order'] = ''
    
        if self.position:
            options_json['version'] += ["company"]
        else:
            options_json['version'] += ["nocompany"]

        return options_json

    def filename(self):
        un = jobdata.funcs.clean(self.person.user.email)
        
        if self.position:
            company_clean = jobdata.funcs.clean(self.position.company.name)
            position_clean = jobdata.funcs.clean(self.position.name)
            fn = os.path.join(
                    'documents',
                    un,
                    company_clean,
                    position_clean,
                    self.template.path
                    )
            fn1 = "___".join([
                    'documents',
                    un,
                    company_clean,
                    position_clean,
                    self.template.path
                    ])
        else:
            fn = os.path.join(
                    'documents',
                    un,
                    'no_company',
                    self.template.path
                    )
            fn1 = "___".join([
                    'documents',
                    un,
                    'no_company',
                    self.template.path
                    ])

        return fn

    def file_write_str(self, s):
        fn = self.filename()

        h,t = os.path.split(fn)

        ab = os.path.join(settings.MEDIA_ROOT, h)
        try:
            os.makedirs(ab)
        except:
            pass

        cf = django.core.files.base.ContentFile(s)

        self.file.save(t, cf)
        #self.file.save(fn, cf)
        
        # make pdf from html files
        
        # get the actual filename from django and split the extension
        h,t = os.path.splitext(self.file.name)

        if t == '.html':
            print "convert pdf"
            print "   ",self.file.name
            cmd = [
                    'wkhtmltopdf',
                    '-q',
                    os.path.join(settings.MEDIA_ROOT, h + '.html'),
                    os.path.join(settings.MEDIA_ROOT, h + '.pdf'),
                    ]

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

            output = p.communicate()
            print "output"
            print output

    def __unicode__(self):
        return "{0:_>40}{1:_>40}{2:_>40}".format(
                str(self.person),
                str(self.template.path),
                str(self.position)
                )


class Position(models.Model):
    name    = models.CharField(max_length=256)
    company = models.ForeignKey('Company')
    def __unicode__(self):
        return "{} --- {} --- {}".format(
                self.id,
                self.company.name,
                self.name)

    def _documents(self):
        return Document.objects.filter(position=self)

    documents = property(_documents)
    

class Company(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

    def _positions(self):
        return Position.objects.filter(company=self)

    positions = property(_positions)

