#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: eyoo_service
    @description:
    @version: 2016-10-06 21:52,validators V1.0 
"""
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import re
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy


@deconstructible
class MobileValidator(object):
    message = ugettext_lazy('请输入合法的手机地址.')
    code = 'invalid'
    regex = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$')

    def __init__(self, message=None, code=None ):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        value = force_text(value)

        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, MobileValidator) and
            (self.domain_whitelist == other.domain_whitelist) and
            (self.message == other.message) and
            (self.code == other.code)
        )