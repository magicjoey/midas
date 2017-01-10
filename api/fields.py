#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: eyoo_service
    @description:
    @version: 2016-10-06 21:49,fields V1.0 
"""
from django.utils.translation import ugettext_lazy
from rest_framework.fields import CharField
from api.validators import MobileValidator


class MobileField(CharField):
    default_error_messages = {
        'invalid': ugettext_lazy('手机号格式不正确.')
    }

    def __init__(self, **kwargs):
        super(MobileField, self).__init__(**kwargs)
        validator = MobileValidator(message=self.error_messages['invalid'])
        self.validators.append(validator)


