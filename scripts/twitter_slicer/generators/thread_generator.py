"""Generate tweet threads from longer content."""

import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THREAD_MAX_TWEETS, OPENROUTER_API_KEY, OPENROUTER_MODEL


class ThreadGenerator:
    """Generate multi-tweet threads from chapter content or stories."""

    @staticmethod
    def from_chapter_slices(slices, chapter_num, chapter_title, lang='zh'):
        """Build a thread from chapter content slices."""
        thread = []

        if lang == 'zh':
            # Tweet 1: Chapter intro
            hook = f"🧵 比特币那些事儿 · 第{chapter_num}章：{chapter_title}\n\n"
            if slices.get('hooks'):
                hook += slices['hooks'][0]
            thread.append(hook)

            # Tweet 2-3: Dramatic moments
            for drama in slices.get('dramatic', [])[:2]:
                thread.append(drama)

            # Tweet 3-4: Fun facts
            for fact in slices.get('facts', [])[:1]:
                thread.append(f"📊 {fact}")

            # Final tweet: CTA
            cta = f"📖 想看完整故事？\n\n全文阅读 → beihaili.github.io/Stories-about-Bitcoin/zh/"
            thread.append(cta)
        else:
            hook = f"🧵 Stories about Bitcoin · Ch.{chapter_num}: {chapter_title}\n\n"
            if slices.get('hooks'):
                hook += slices['hooks'][0]
            thread.append(hook)

            for drama in slices.get('dramatic', [])[:2]:
                thread.append(drama)

            for fact in slices.get('facts', [])[:1]:
                thread.append(f"📊 {fact}")

            cta = f"📖 Read the full story → beihaili.github.io/Stories-about-Bitcoin/en/"
            thread.append(cta)

        return thread[:THREAD_MAX_TWEETS]

    @staticmethod
    def from_story(story_data, lang='zh'):
        """Build a thread from a processed legendary story."""
        if lang == 'zh':
            return story_data.get('thread_zh', [])[:THREAD_MAX_TWEETS]
        # English threads would need translation (LLM or manual)
        return story_data.get('thread_zh', [])[:THREAD_MAX_TWEETS]

    @staticmethod
    def polish_with_llm(tweets, style='engaging', lang='zh'):
        """Optional: polish tweet text using LLM via OpenRouter."""
        if not OPENROUTER_API_KEY:
            print("[thread_generator] No OPENROUTER_API_KEY set, skipping LLM polish")
            return tweets

        try:
            from openai import OpenAI
        except ImportError:
            print("[thread_generator] openai package not installed, skipping LLM polish")
            return tweets

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

        prompt = f"""You are a Twitter content expert for a Bitcoin history book.
Polish the following tweet thread to be more {style} while keeping the same information.
Each tweet must stay under 280 characters. Keep the language as {'Chinese' if lang == 'zh' else 'English'}.
Return only the polished tweets, one per line, separated by ---

Thread:
"""
        for i, t in enumerate(tweets):
            prompt += f"\nTweet {i+1}:\n{t}\n"

        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )

        result_text = response.choices[0].message.content
        polished = [t.strip() for t in result_text.split('---') if t.strip()]

        # Validate: must have same number of tweets
        if len(polished) != len(tweets):
            print(f"[thread_generator] LLM returned {len(polished)} tweets, expected {len(tweets)}. Using original.")
            return tweets

        return polished
