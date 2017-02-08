from core import model_mixins as mixins


def update_votes_count(sender, instance, created, **kwargs):
    voted_class = instance.content_object.__class__
    if issubclass(voted_class, mixins.VoteCountMixin):
        if created:
            if instance.vote:
                instance.content_object.upvote_count += 1
            else:
                instance.content_object.downvote_count += 1
        else:
            if instance.vote:
                instance.content_object.upvote_count += 1
                instance.content_object.downvote_count -= 1
            else:
                instance.content_object.upvote_count -= 1
                instance.content_object.downvote_count += 1

        instance.content_object.save()

    if issubclass(voted_class, mixins.ParticipationCountMixin):
        if created:
            instance.content_object.participation_count += 1
            instance.content_object.save()


def update_comments_count(sender, instance, created, **kwargs):
    commented_class = instance.content_object.__class__
    if created and issubclass(commented_class, mixins.CommentCountMixin):
        instance.content_object.comments_count += 1

    if created and issubclass(commented_class, mixins.ParticipationCountMixin):
        instance.content_object.participation_count += 1

    instance.content_object.save()


def update_additive_amendment_count(sender, instance, created, **kwargs):
    if created:
        instance.reference.amendments_count += 1
        instance.reference.participation_count += 1
        instance.reference.additive_amendments_count += 1
        instance.reference.save()

        instance.reference.bill.amendments_count += 1
        instance.reference.bill.save()


def update_modifier_amendment_count(sender, instance, created, **kwargs):
    if created:
        instance.replaced.amendments_count += 1
        instance.replaced.participation_count += 1
        instance.replaced.modifier_amendments_count += 1
        instance.replaced.save()

        instance.replaced.bill.amendments_count += 1
        instance.replaced.bill.save()


def update_supress_amendment_count(sender, instance, created, **kwargs):
    if created:
        instance.supressed.amendments_count += 1
        instance.supressed.participation_count += 1
        instance.supressed.supress_amendments_count += 1
        instance.supressed.save()

        instance.supressed.bill.amendments_count += 1
        instance.supressed.bill.save()
