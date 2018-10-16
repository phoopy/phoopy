from datetime import datetime, timedelta


class DateSpan(object):
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return '[{}, {}]'.format(
            self.start_date.strftime('%Y-%m-%d') if self.start_date else '',
            self.end_date.strftime('%Y-%m-%d') if self.end_date else ''
        )


class DateHelper(object):
    @staticmethod
    def is_valid_date(value):
        result = True
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            result = False
        return result

    @staticmethod
    def split_date_interval(start_date, end_date, span_delta):
        spans = []
        actual_span = DateSpan(start_date, None)
        while actual_span.end_date is None or actual_span.end_date < end_date:
            next_date = actual_span.start_date + span_delta
            if next_date > end_date:
                next_date = end_date
            actual_span.end_date = next_date
            spans.append(actual_span)
            if actual_span.end_date < end_date:
                actual_span = DateSpan(
                    actual_span.end_date + timedelta(days=1),
                    None
                )
        return spans
