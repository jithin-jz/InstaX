from instagrapi import Client
import time
import random
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class InstagramBot:
    def __init__(self, username, password):
        self.client = Client()
        self.username = username
        self.password = password
        self.action_count = 0  # Track actions to avoid limits
        self.login()

    def login(self):
        """Log in to Instagram."""
        try:
            self.client.login(self.username, self.password)
            print(f"{Fore.GREEN}✅ Logged in as {Fore.CYAN}{self.username}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Login failed: {e}{Style.RESET_ALL}")
            raise

    def logout(self):
        """Log out of Instagram."""
        self.client.logout()
        print(f"{Fore.GREEN}✅ Logged out{Style.RESET_ALL}")

    def _random_delay(self, min_sec=10, max_sec=30):
        """Add a random delay between actions to mimic human behavior."""
        delay = random.randint(min_sec, max_sec)
        print(f"{Fore.YELLOW}⏳ Waiting for {delay} seconds...{Style.RESET_ALL}")
        time.sleep(delay)

    def _increment_action_count(self):
        """Increment the action counter."""
        self.action_count += 1
        print(f"{Fore.YELLOW}📊 Total actions today: {self.action_count}{Style.RESET_ALL}")

    def like_posts_by_hashtag(self, hashtag, count=5):
        """Like posts from a specific hashtag."""
        try:
            print(f"{Fore.BLUE}🔍 Searching for posts with hashtag: {Fore.MAGENTA}#{hashtag}{Style.RESET_ALL}")
            posts = self.client.hashtag_medias_recent(hashtag, amount=count)
            for post in posts:
                if self.action_count >= 300:
                    print(f"{Fore.RED}⚠️ Daily like limit reached. Stopping...{Style.RESET_ALL}")
                    return
                self.client.media_like(post.id)
                print(f"{Fore.GREEN}❤️ Liked post: {Fore.CYAN}{post.code}{Style.RESET_ALL}")
                self._increment_action_count()
                self._random_delay()
        except Exception as e:
            print(f"{Fore.RED}❌ Error liking posts: {e}{Style.RESET_ALL}")

    def follow_followers_of_account(self, target_user, limit=5):
        """Follow followers of a specific account."""
        try:
            print(f"{Fore.BLUE}🔍 Finding followers of: {Fore.CYAN}{target_user}{Style.RESET_ALL}")
            user_id = self.client.user_id_from_username(target_user)
            followers = self.client.user_followers(user_id, amount=limit)
            for user in followers.values():
                if self.action_count >= 100:
                    print(f"{Fore.RED}⚠️ Daily follow limit reached. Stopping...{Style.RESET_ALL}")
                    return
                try:
                    self.client.user_follow(user.pk)
                    print(f"{Fore.GREEN}✅ Followed {Fore.CYAN}{user.username}{Style.RESET_ALL}")
                    self._increment_action_count()
                    self._random_delay()
                except Exception as e:
                    if "feedback_required" in str(e):
                        print(f"{Fore.RED}⚠️ Action blocked. Waiting 1 hour...{Style.RESET_ALL}")
                        time.sleep(3600)
                    else:
                        print(f"{Fore.RED}❌ Error following: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

    def unfollow_non_followers(self):
        """Unfollow users who don't follow back."""
        try:
            print(f"{Fore.BLUE}🔍 Finding non-followers...{Style.RESET_ALL}")
            following = self.client.user_following(self.client.user_id)
            followers = self.client.user_followers(self.client.user_id)
            
            following_ids = set(following.keys())
            followers_ids = set(followers.keys())
            non_followers = following_ids - followers_ids

            for user_id in list(non_followers)[:10]:
                if self.action_count >= 100:
                    print(f"{Fore.RED}⚠️ Daily unfollow limit reached{Style.RESET_ALL}")
                    return
                self.client.user_unfollow(user_id)
                username = following[user_id].username
                print(f"{Fore.RED}❌ Unfollowed {Fore.CYAN}{username}{Style.RESET_ALL}")
                self._increment_action_count()
                self._random_delay()
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

    def comment_on_latest_posts_of_followed_accounts(self, comment="Great post! 👏"):
        """Like + comment on latest posts of followed accounts."""
        try:
            print(f"{Fore.BLUE}🔍 Checking followed accounts...{Style.RESET_ALL}")
            following = self.client.user_following(self.client.user_id)
            for user in following.values():
                if self.action_count >= 50:
                    print(f"{Fore.RED}⚠️ Daily comment limit reached{Style.RESET_ALL}")
                    return
                try:
                    posts = self.client.user_medias(user.pk, amount=1)
                    if posts:
                        post = posts[0]
                        # Like
                        self.client.media_like(post.pk)
                        print(f"{Fore.GREEN}❤️ Liked {Fore.CYAN}{user.username}'s post{Style.RESET_ALL}")
                        # Comment
                        self.client.media_comment(post.pk, comment)
                        print(f"{Fore.GREEN}💬 Commented on {Fore.CYAN}{user.username}'s post{Style.RESET_ALL}")
                        self._increment_action_count()
                        self._random_delay()
                except Exception as e:
                    print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

    def follow_unfollow_target_every_30_sec(self, target_user):
        """Follow + unfollow target account every 30 seconds."""
        try:
            print(f"{Fore.BLUE}🔄 Auto follow/unfollow: {Fore.CYAN}{target_user}{Style.RESET_ALL}")
            while True:
                start_time = time.time()
                if self.action_count >= 100:
                    print(f"{Fore.RED}⚠️ Daily action limit reached{Style.RESET_ALL}")
                    return
                
                try:
                    user_id = self.client.user_id_from_username(target_user)
                    # Follow
                    self.client.user_follow(user_id)
                    print(f"{Fore.GREEN}✅ Followed {Fore.CYAN}{target_user}{Style.RESET_ALL}")
                    self._increment_action_count()
                    time.sleep(random.randint(5, 10))  # Random delay between actions
                    
                    # Unfollow
                    self.client.user_unfollow(user_id)
                    print(f"{Fore.RED}❌ Unfollowed {Fore.CYAN}{target_user}{Style.RESET_ALL}")
                    self._increment_action_count()
                    
                    # Maintain 30-second cycle
                    elapsed = time.time() - start_time
                    if elapsed < 30:
                        time.sleep(30 - elapsed)
                except Exception as e:
                    print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Critical error: {e}{Style.RESET_ALL}")

    def view_stories_of_all_users(self):
        """View stories of all followed accounts."""
        try:
            print(f"{Fore.BLUE}👀 Viewing stories...{Style.RESET_ALL}")
            following = self.client.user_following(self.client.user_id)
            for user in following.values():
                try:
                    stories = self.client.user_stories(user.pk)
                    if stories:
                        story_pks = [s.pk for s in stories]
                        self.client.story_seen(story_pks)
                        print(f"{Fore.GREEN}📸 Viewed {len(story_pks)} stories by {Fore.CYAN}{user.username}{Style.RESET_ALL}")
                        self._random_delay()
                except Exception as e:
                    print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

    def dm_new_followers(self, message="Thanks for following!"):
        """DM new followers."""
        try:
            print(f"{Fore.BLUE}📩 Messaging new followers...{Style.RESET_ALL}")
            followers = self.client.user_followers(self.client.user_id)
            for user in followers.values():
                if self.action_count >= 50:
                    print(f"{Fore.RED}⚠️ Daily DM limit reached{Style.RESET_ALL}")
                    return
                self.client.direct_send(message, user_ids=[user.pk])
                print(f"{Fore.GREEN}✅ DM sent to {Fore.CYAN}{user.username}{Style.RESET_ALL}")
                self._increment_action_count()
                self._random_delay()
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

    def is_following_user(self, target_user):
        """Check if following a user."""
        try:
            user_id = self.client.user_id_from_username(target_user)
            return user_id in self.client.user_following(self.client.user_id)
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            return False

def display_menu():
    """Display interactive menu."""
    print(f"\n{Fore.BLUE}━━━━ Instagram Bot ━━━━{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. Like Posts by Hashtag")
    print(f"2. Follow Followers of Target")
    print(f"3. Unfollow Non-Followers")
    print(f"4. Engage with Followed Accounts")
    print(f"5. View Stories")
    print(f"6. Auto Follow/Unfollow Target")
    print(f"7. DM New Followers")
    print(f"8. Exit{Style.RESET_ALL}")
    return input(f"{Fore.CYAN}Choose option (1-8): {Style.RESET_ALL}")

def main():
    """Main function to run the bot."""
    try:
        # Credentials
        username = input(f"{Fore.CYAN}Username: {Style.RESET_ALL}")
        password = input(f"{Fore.CYAN}Password: {Style.RESET_ALL}")
        bot = InstagramBot(username, password)

        # Initial follow check
        target_user = "jithin.jz"
        print(f"{Fore.BLUE}⚠️ First follow @{target_user} to continue!{Style.RESET_ALL}")
        while not bot.is_following_user(target_user):
            print(f"{Fore.RED}❌ Not following @{target_user} - checking again in 10s...{Style.RESET_ALL}")
            time.sleep(10)

        # Main loop
        while True:
            choice = display_menu()
            
            if choice == "1":
                hashtag = input("Enter hashtag: ").strip("#")
                bot.like_posts_by_hashtag(hashtag, 5)
            
            elif choice == "2":
                target = input("Target username: ")
                bot.follow_followers_of_account(target, 5)
            
            elif choice == "3":
                bot.unfollow_non_followers()
            
            elif choice == "4":
                comment = input("Enter comment: ")
                bot.comment_on_latest_posts_of_followed_accounts(comment)
            
            elif choice == "5":
                bot.view_stories_of_all_users()
            
            elif choice == "6":
                target = input("Target username: ")
                bot.follow_unfollow_target_every_30_sec(target)
            
            elif choice == "7":
                msg = input("Enter DM message: ")
                bot.dm_new_followers(msg)
            
            elif choice == "8":
                bot.logout()
                print(f"{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}🚨 Critical error: {e}{Style.RESET_ALL}")
    finally:
        print(f"{Fore.YELLOW}⚠️ Session ended{Style.RESET_ALL}")

if __name__ == "__main__":
    main()