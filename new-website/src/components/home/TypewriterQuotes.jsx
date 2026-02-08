import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const TypewriterQuotes = ({ lang = 'zh' }) => {
  const quotes = {
    zh: [
      { text: '"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"', author: '中本聪 · 创世区块' },
      { text: '"如果你不相信我或者理解不了，我没有时间去说服你，抱歉。"', author: '中本聪' },
      { text: '"货币的非国家化——私人发行的竞争性货币才是理想形态"', author: '弗里德里希·哈耶克' },
      { text: '"我们必须信任银行来保管我们的钱...但他们却在信用泡沫中将其借出"', author: '中本聪' },
      { text: '"Running bitcoin"', author: '哈尔·芬尼 · 第一条比特币推文' },
    ],
    en: [
      { text: '"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"', author: 'Satoshi Nakamoto · Genesis Block' },
      { text: '"If you don\'t believe me or don\'t get it, I don\'t have time to try to convince you, sorry."', author: 'Satoshi Nakamoto' },
      { text: '"The denationalization of money — privately issued competing currencies are the ideal form"', author: 'Friedrich Hayek' },
      { text: '"We have to trust banks with our money... but they lend it out in waves of credit bubbles"', author: 'Satoshi Nakamoto' },
      { text: '"Running bitcoin"', author: 'Hal Finney · First Bitcoin Tweet' },
    ]
  };

  const [currentIndex, setCurrentIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);
  const containerRef = useRef(null);
  const isVisibleRef = useRef(true);

  const currentQuotes = quotes[lang];
  const currentQuote = currentQuotes[currentIndex];

  // IntersectionObserver to pause when offscreen
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => { isVisibleRef.current = entry.isIntersecting; },
      { threshold: 0, rootMargin: '100px' }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    let timeout;

    const tick = () => {
      if (!isVisibleRef.current) {
        timeout = setTimeout(tick, 200);
        return;
      }

      if (!isDeleting) {
        if (displayedText.length < currentQuote.text.length) {
          setDisplayedText(currentQuote.text.slice(0, displayedText.length + 1));
        } else {
          timeout = setTimeout(() => setIsDeleting(true), 3000);
          return;
        }
      } else {
        if (displayedText.length > 0) {
          setDisplayedText(displayedText.slice(0, -1));
        } else {
          setIsDeleting(false);
          setCurrentIndex((prev) => (prev + 1) % currentQuotes.length);
          return;
        }
      }
    };

    timeout = setTimeout(tick, isDeleting ? 25 : 50);

    return () => clearTimeout(timeout);
  }, [displayedText, isDeleting, currentQuote.text, currentQuotes.length]);

  return (
    <div ref={containerRef} className="min-h-[120px] sm:min-h-[100px] flex flex-col items-center justify-center">
      <motion.div
        className="text-base sm:text-lg md:text-xl text-historical-antique max-w-3xl mx-auto leading-relaxed px-4 text-center font-serif italic"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <span>{displayedText}</span>
        <motion.span
          className="inline-block w-0.5 h-5 sm:h-6 bg-bitcoin-orange ml-1"
          animate={{ opacity: [1, 0] }}
          transition={{ duration: 0.5, repeat: Infinity }}
        />
      </motion.div>

      <AnimatePresence mode="wait">
        <motion.p
          key={currentIndex}
          className="text-sm text-bitcoin-darkGold mt-3 font-medium"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.3 }}
        >
          — {currentQuote.author}
        </motion.p>
      </AnimatePresence>
    </div>
  );
};

export default TypewriterQuotes;
