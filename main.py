import random
import time
import configparser
import logging
from instabot import Bot
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, exc
from datetime import datetime, timedelta

# ---------------------- Configuration ----------------------

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.INSTA_USERNAME = self.config['INSTAGRAM']['USERNAME']
        self.INSTA_PASSWORD = self.config['INSTAGRAM']['PASSWORD']
        self.HASHTAGS = self.config['SETTINGS']['HASHTAGS'].split(',')
        self.LIKE_AMOUNT = int(self.config['SETTINGS']['LIKE_AMOUNT'])
        self.DELAY_BETWEEN_LIKES = int(self.config['SETTINGS']['DELAY_BETWEEN_LIKES'])
        self.DELAY_BETWEEN_COMMENTS = int(self.config['SETTINGS']['DELAY_BETWEEN_COMMENTS'])
        self.UNFOLLOW_AFTER_DAYS = int(self.config['SETTINGS']['UNFOLLOW_AFTER_DAYS'])
        self.COMMENTS_LIST = self.config['SETTINGS']['COMMENTS_LIST'].split(',')


# ---------------------- Logging Setup ----------------------

logging.basicConfig(filename='bot.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------------- Database Setup ----------------------

Base = declarative_base()

class LikedPost(Base):
    __tablename__ = 'liked_posts'
    id = Column(Integer, Sequence('liked_post_id_seq'), primary_key=True)
    post_id = Column(String(50))

engine = create_engine('sqlite:///bot_database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# ---------------------- Bot Operations ----------------------

class InstaBotOps:
    def __init__(self, config: Config):
        self.config = config
        self.bot = Bot()

    def _get_random_comment(self) -> str:
        """Retrieve a random comment from the comments list."""
        return random.choice(self.config.COMMENTS_LIST)

    def _should_engage_with_user(self, user_id: str) -> bool:
        """Decide whether to engage with a user based on certain criteria."""
        user_info = self.bot.get_user_info(user_id)
        return user_info["follower_count"] / (user_info["following_count"] + 1) > 0.5

    def _unfollow_non_followers(self):
        """Unfollow users who aren't following back after a specified duration."""
        non_followers = set(self.bot.following) - set(self.bot.followers)
        for user_id in non_followers:
            followed_duration = datetime.now() - self.bot.get_following_status(user_id)["followed_at"]
            if followed_duration > timedelta(days=self.config.UNFOLLOW_AFTER_DAYS):
                self.bot.unfollow(user_id)

    def run_bot_operations(self):
        """Main method to execute bot operations."""
        try:
            self.bot.login(username=self.config.INSTA_USERNAME, password=self.config.INSTA_PASSWORD)
            self._unfollow_non_followers()

            for hashtag in self.config.HASHTAGS:
                for post in self.bot.get_hashtag_medias(hashtag, amount=self.config.LIKE_AMOUNT):
                    user_id = self.bot.get_media_owner(post)
                    if not self._should_engage_with_user(user_id):
                        continue

                    with Session() as session:
                        if not session.query(LikedPost).filter_by(post_id=post).count():
                            self.bot.like(post)
                            time.sleep(self.config.DELAY_BETWEEN_LIKES)
                            self.bot.comment(post, self._get_random_comment())
                            time.sleep(self.config.DELAY_BETWEEN_COMMENTS)
                            self.bot.follow(user_id)
                            session.add(LikedPost(post_id=post))
                            session.commit()

            self.bot.logout()

        except exc.SQLAlchemyError as db_error:
            logging.error(f"Database error occurred: {db_error}")
        except Exception as e:
            logging.error(f"Error occurred: {e}")
        finally:
            logging.info("Bot finished its run!")

# ---------------------- Main Execution ----------------------

if __name__ == '__main__':
    config = Config()
    bot_ops = InstaBotOps(config)
    bot_ops.run_bot_operations()
