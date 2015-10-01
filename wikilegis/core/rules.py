# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import rules
from rules.predicates import is_superuser, is_staff
from wikilegis.core.models import Bill


@rules.predicate
def is_bill_editor(user, bill):
    if bill is None:
        return Bill.objects.filter(editors__pk__in=user.groups.values('pk')).count()
    else:
        return user.groups.filter(pk__in=bill.editors.values('pk')).count() > 0


@rules.predicate
def is_segment_editor(user, segment):
    return is_bill_editor(user, segment.bill if segment else None)


rules.add_perm('core.change_bill', is_superuser | is_staff & is_bill_editor)
rules.add_perm('core.add_billsegment', is_superuser | is_staff & is_segment_editor)
rules.add_perm('core.change_billsegment', is_superuser | is_staff & is_segment_editor)
rules.add_perm('core.delete_billsegment', is_superuser | is_staff & is_segment_editor)
