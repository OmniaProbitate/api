from prkng.database import db


class Analytics(object):
    @staticmethod
    def get_user_data():
        today = db.engine.execute("""
            SELECT count(id)
            FROM users
            WHERE (created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern' >= (NOW() AT TIME ZONE 'US/Eastern')::date
              AND (created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern' <= (NOW() AT TIME ZONE 'US/Eastern' + INTERVAL '1 DAY')::date
        """).first()[0]
        week = db.engine.execute("""
            SELECT
              a.date, count(u.id)
            FROM (
              SELECT
                to_char(date_trunc('day', ((NOW() AT TIME ZONE 'US/Eastern')::date - (offs * INTERVAL '1 DAY'))), 'YYYY-MM-DD"T"HH24:MI:SS"-0400"') AS date
              FROM generate_series(0, 365, 1) offs
            ) a
            LEFT OUTER JOIN users u
              ON (a.date = to_char(date_trunc('day', (u.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern'), 'YYYY-MM-DD"T"HH24:MI:SS"-0400"'))
            GROUP BY a.date
            ORDER BY a.date DESC
            OFFSET 1 LIMIT 6
        """)
        year = db.engine.execute("""
            SELECT
              to_char(a.date, 'Mon'), count(u.id)
            FROM (
              SELECT
                date_trunc('month', ((NOW() AT TIME ZONE 'US/Eastern')::date - (offs * INTERVAL '1 MONTH'))) AS date
              FROM generate_series(0, 12, 1) offs
            ) a
            LEFT OUTER JOIN users u
              ON (to_char(a.date, 'Mon') = to_char(date_trunc('month', (u.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern'), 'Mon'))
            GROUP BY a.date
            ORDER BY a.date DESC
            LIMIT 6
        """)
        return {"day": today, "week": [{key: value for key, value in row.items()} for row in week],
            "year": [{key: value for key, value in row.items()} for row in year]}

    @staticmethod
    def get_active_user_chk_data():
        today = db.engine.execute("""
            SELECT count(DISTINCT u.id)
            FROM users u
            JOIN checkins c ON u.id = c.user_id
            WHERE (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern' >= (NOW() AT TIME ZONE 'US/Eastern')::date
              AND (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern' <= (NOW() AT TIME ZONE 'US/Eastern' + INTERVAL '1 DAY')::date
        """).first()[0]
        week = db.engine.execute("""
            SELECT
              a.date, count(DISTINCT c.user_id)
            FROM (
              SELECT
                to_char(date_trunc('day', ((NOW() AT TIME ZONE 'US/Eastern')::date - (offs * INTERVAL '1 DAY'))), 'YYYY-MM-DD"T"HH24:MI:SS"-0400"') AS date
              FROM generate_series(0, 365, 1) offs
            ) a
            LEFT OUTER JOIN checkins c
              ON (a.date = to_char(date_trunc('day', (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern'), 'YYYY-MM-DD"T"HH24:MI:SS"-0400"'))
            GROUP BY a.date
            ORDER BY a.date DESC
            OFFSET 1 LIMIT 6
        """)
        year = db.engine.execute("""
            SELECT
              to_char(a.date, 'Mon'), count(DISTINCT c.user_id)
            FROM (
              SELECT
                date_trunc('month', ((NOW() AT TIME ZONE 'US/Eastern')::date - (offs * INTERVAL '1 MONTH'))) AS date
              FROM generate_series(0, 12, 1) offs
            ) a
            LEFT OUTER JOIN checkins c
              ON (to_char(a.date, 'Mon') = to_char(date_trunc('month', (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern'), 'Mon'))
            GROUP BY a.date
            ORDER BY a.date DESC
            LIMIT 6
        """)
        return {"day": today, "week": [{key: value for key, value in row.items()} for row in week],
            "year": [{key: value for key, value in row.items()} for row in year]}

    @staticmethod
    def get_active_user_data():
        today = db.engine.execute("""
            SELECT count(DISTINCT c.user_id)
            FROM analytics_pos c
            WHERE (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern' >= (NOW() AT TIME ZONE 'US/Eastern')::date
              AND (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern' <= (NOW() AT TIME ZONE 'US/Eastern' + INTERVAL '1 DAY')::date
        """).first()[0]
        week = db.engine.execute("""
            SELECT
              a.date, count(DISTINCT c.user_id)
            FROM (
              SELECT
                to_char(date_trunc('day', ((NOW() AT TIME ZONE 'US/Eastern')::date - (offs * INTERVAL '1 DAY'))), 'YYYY-MM-DD"T"HH24:MI:SS"-0400"') AS date
              FROM generate_series(0, 365, 1) offs
            ) a
            LEFT OUTER JOIN analytics_pos c
              ON (a.date = to_char(date_trunc('day', (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern'), 'YYYY-MM-DD"T"HH24:MI:SS"-0400"'))
            GROUP BY a.date
            ORDER BY a.date DESC
            OFFSET 1 LIMIT 6
        """)
        year = db.engine.execute("""
            SELECT
              to_char(a.date, 'Mon'), count(DISTINCT c.user_id)
            FROM (
              SELECT
                date_trunc('month', ((NOW() AT TIME ZONE 'US/Eastern')::date - (offs * INTERVAL '1 MONTH'))) AS date
              FROM generate_series(0, 12, 1) offs
            ) a
            LEFT OUTER JOIN analytics_pos c
              ON (to_char(a.date, 'Mon') = to_char(date_trunc('month', (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern'), 'Mon'))
            GROUP BY a.date
            ORDER BY a.date DESC
            LIMIT 6
        """)
        return {"day": today, "week": [{key: value for key, value in row.items()} for row in week],
            "year": [{key: value for key, value in row.items()} for row in year]}

    @staticmethod
    def get_checkin_data():
        today = db.engine.execute("""
            SELECT count(id)
            FROM checkins
            WHERE (created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern' >= (NOW() AT TIME ZONE 'US/Eastern')::date
              AND (created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern' <= (NOW() AT TIME ZONE 'US/Eastern' + INTERVAL '1 DAY')::date
        """).first()[0]
        week = db.engine.execute("""
            SELECT
              a.date, count(c.id)
            FROM (
              SELECT
                to_char(date_trunc('day', ((NOW() AT TIME ZONE 'US/Eastern')::date - (offs * INTERVAL '1 DAY'))), 'YYYY-MM-DD"T"HH24:MI:SS"-0400"') AS date
              FROM generate_series(0, 365, 1) offs
            ) a
            LEFT OUTER JOIN checkins c
              ON (a.date = to_char(date_trunc('day', (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern'), 'YYYY-MM-DD"T"HH24:MI:SS"-0400"'))
            GROUP BY a.date
            ORDER BY a.date DESC
            OFFSET 1 LIMIT 6
        """)
        year = db.engine.execute("""
            SELECT
              to_char(a.date, 'Mon'), count(c.id)
            FROM (
              SELECT
                date_trunc('month', ((NOW() AT TIME ZONE 'US/Eastern')::date - (offs * INTERVAL '1 MONTH'))) AS date
              FROM generate_series(0, 12, 1) offs
            ) a
            LEFT OUTER JOIN checkins c
              ON (to_char(a.date, 'Mon') = to_char(date_trunc('month', (c.created AT TIME ZONE 'UTC') AT TIME ZONE 'US/Eastern'), 'Mon'))
            GROUP BY a.date
            ORDER BY a.date DESC
            LIMIT 6
        """)
        return {"day": today, "week": [{key: value for key, value in row.items()} for row in week],
            "year": [{key: value for key, value in row.items()} for row in year]}

    @staticmethod
    def get_map_usage(hours=24):
        res = db.engine.execute("""
            SELECT lat, long, 1 AS value
            FROM analytics_pos
            WHERE created >= (NOW() - ({} * INTERVAL '1 HOUR'))
        """.format(hours))
        return [{key: value for key, value in row.items()} for row in res]

    @staticmethod
    def get_geofence_checks():
        res = db.engine.execute("""
            SELECT DISTINCT ON (ae.user_id, ae.created)
                ae.id,
                to_char(c.created, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS checkin_time,
                to_char(ae.created, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS response_time,
                ae.user_id,
                u.name,
                c.lat,
                c.long,
                CASE ae.event WHEN 'fence_response_yes' THEN true ELSE false END AS checkout
            FROM analytics_event ae
            JOIN users u ON ae.user_id = u.id
            JOIN checkins c ON ae.user_id = c.user_id AND ae.created >= c.created
            WHERE ae.event LIKE '%%fence_response%%'
            ORDER BY ae.user_id, ae.created DESC, c.created DESC
        """)
        return [{key: value for key, value in row.items()} for row in res]
