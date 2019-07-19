

def segment_stats(segment):
    ids = []
    comments_count = segment.comments_count
    amendment_votes = 0

    ids += list(segment.modifier_amendments.values_list(
        'author__id', flat=True
    ))
    for amendment in segment.modifier_amendments.all():
        ids += list(amendment.comments.values_list('author__id', flat=True))
        comments_count += amendment.comments_count
        amendment_votes += amendment.votes_count

    ids += list(segment.additive_amendments.values_list(
        'author__id', flat=True
    ))
    for amendment in segment.additive_amendments.all():
        ids += list(amendment.comments.values_list('author__id', flat=True))
        comments_count += amendment.comments_count
        amendment_votes += amendment.votes_count

    ids += list(segment.supress_amendments.values_list(
        'author__id', flat=True
    ))
    for amendment in segment.supress_amendments.all():
        ids += list(amendment.comments.values_list('author__id', flat=True))
        comments_count += amendment.comments_count
        amendment_votes += amendment.votes_count

    ids += list(segment.comments.values_list('author__id', flat=True))

    return {
        'participants': len(set(ids)),
        'participants_ids': set(ids),
        'amendment_votes': amendment_votes,
        'segment_votes': segment.votes_count,
        'additive_amendments': segment.additive_amendments_count,
        'supress_amendments': segment.supress_amendments_count,
        'modifier_amendments': segment.modifier_amendments_count,
        'comments_count': comments_count
    }


def bill_stats(bill):
    ids = []
    segment_votes = 0
    amendment_votes = 0
    bill_votes = bill.votes_count
    additive_count = 0
    supress_count = 0
    modifier_count = 0
    comments_count = 0

    for segment in bill.segments.all():
        stats = segment_stats(segment)
        ids += list(stats['participants_ids'])
        segment_votes += stats['segment_votes']
        amendment_votes += stats['amendment_votes']
        additive_count += stats['additive_amendments']
        modifier_count += stats['modifier_amendments']
        supress_count += stats['supress_amendments']
        comments_count += stats['comments_count']

    ids += list(bill.votes.values_list('user__id', flat=True))

    return {
        'participants_count': len(set(ids)),
        'segment_votes': segment_votes,
        'amendment_votes': amendment_votes,
        'comments_count': comments_count,
        'bill_votes': bill_votes,
        'additive_count': additive_count,
        'supress_count': supress_count,
        'modifier_count': modifier_count,
        'amendments_count': additive_count + supress_count + modifier_count,
    }
