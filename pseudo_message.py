class PseudoMessage():
    def __init__(self, cmd):
        self.guild = _fake_guild()
        self.channel = _fake_channel()
        self.author = _fake_author()
        self.content = cmd
        self._state = None

class _fake_guild():
    def __init__(self):
        self.name = 'CLI'
        self.id = 1
        self.owner_id = 0xdeadbeef
        self.unavailable = False
        self.emojis = ()
        self.region = None
        self.afk_timeout = 0
        self.afk_channel = None
        self.mfa_level = 0
        self.features = []
        self.verification_level = None
        self.explicit_content_filter = None
        self.default_notifications = None
        self.premium_tier = 0
        self.premium_subscription_count = 0
        self.discovert_splash = ""

class _fake_author():
    def __init__(self):
        self.name = 'ConsoleUser'
        self.id = 0xdeadbeef
        self.discriminator = 1234
        self.avatar = None
        self.bot = False
        self.system = False
        self.guild = _fake_guild()
        self.joined_at = None
        self.premium_since = None
        self.activities = ()
        self.nick = None

    def __str__(self):
        return '{0.name}#{0.discriminator}'.format(self)

class _fake_channel():
    def __init__(self):
        self.name = 'Console'
        self.guild = _fake_guild()
        self.id = 2
        self.category_id = None
        self.topic = None
        self.position = 0
        self.last_message_id = None
        self.slowmode_delay = None

