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
    if created:
        if issubclass(commented_class, mixins.CommentCountMixin):
            instance.content_object.comments_count += 1

        if issubclass(commented_class, mixins.ParticipationCountMixin):
            instance.content_object.participation_count += 1

        instance.content_object.save()
