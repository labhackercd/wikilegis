from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.db.models.signals import post_save, post_delete
        from core import models, signals
        post_save.connect(signals.update_new_votes_count,
                          sender=models.UpDownVote)
        post_delete.connect(signals.update_deleted_votes_count,
                            sender=models.UpDownVote)
        post_save.connect(signals.update_comments_count,
                          sender=models.Comment)
        post_save.connect(signals.update_additive_amendment_count,
                          sender=models.AdditiveAmendment)
        post_save.connect(signals.update_modifier_amendment_count,
                          sender=models.ModifierAmendment)
        post_save.connect(signals.update_supress_amendment_count,
                          sender=models.SupressAmendment)
