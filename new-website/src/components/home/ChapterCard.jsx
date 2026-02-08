import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShareButton } from '../common/ShareButtons';

const ChapterCard = ({ chapter, lang = 'zh', index, markAsRead, isRead }) => {
  const [isHovered, setIsHovered] = useState(false);

  const handleClick = () => {
    const baseUrl = 'https://beihaili.github.io/Stories-about-Bitcoin';
    window.open(`${baseUrl}${chapter.link[lang]}`, '_blank');
    markAsRead?.(chapter.id);
  };

  return (
    <motion.div
      role="article"
      tabIndex={0}
      aria-label={chapter.title[lang]}
      className="chapter-card group relative focus-ring"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: Math.min(index * 0.05, 0.3), duration: 0.5 }}
      whileHover={{ y: -8 }}
      onClick={handleClick}
      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleClick(); } }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Image */}
      <div className="relative h-48 sm:h-56 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-bitcoin-orange to-bitcoin-gold opacity-80 group-hover:opacity-90 transition-opacity duration-300"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.span
            className="text-7xl sm:text-8xl opacity-30"
            animate={{ scale: isHovered ? 1.2 : 1, rotate: isHovered ? 5 : 0 }}
            transition={{ duration: 0.3 }}
          >
            {chapter.icon}
          </motion.span>
        </div>
        {/* Year + reading time labels */}
        <div className="absolute top-3 left-3 sm:top-4 sm:left-4 flex items-center gap-2">
          <span className="bg-white bg-opacity-90 px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-semibold text-historical-sepia">
            {chapter.year || (lang === 'zh' ? '序言' : 'Prologue')}
          </span>
          {chapter.readingTime && (
            <span className="bg-white bg-opacity-90 px-2 py-1 rounded-full text-xs text-historical-antique">
              {chapter.readingTime} {lang === 'zh' ? '分钟' : 'min'}
            </span>
          )}
          {isRead && (
            <span className="bg-green-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
              {lang === 'zh' ? '已读' : 'Read'}
            </span>
          )}
        </div>

        {/* Share button */}
        <div className="absolute top-3 right-3 sm:top-4 sm:right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-200" onClick={(e) => e.stopPropagation()} onKeyDown={(e) => e.stopPropagation()}>
          <ShareButton
            url={`https://beihaili.github.io/Stories-about-Bitcoin${chapter.link[lang]}`}
            title={chapter.title[lang]}
            lang={lang}
          />
        </div>

        {/* Hover Preview Overlay */}
        <AnimatePresence>
          {isHovered && (
            <motion.div
              className="absolute inset-0 bg-black bg-opacity-70 flex items-center justify-center p-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <div className="text-white text-center">
                <p className="text-sm sm:text-base leading-relaxed mb-3">
                  {chapter.summary[lang]}
                </p>
                <motion.span
                  className="inline-flex items-center gap-2 text-bitcoin-gold font-semibold text-sm"
                  animate={{ x: [0, 5, 0] }}
                  transition={{ duration: 1, repeat: Infinity }}
                >
                  {lang === 'zh' ? '点击阅读' : 'Click to Read'}
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </motion.span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Content */}
      <div className="p-4 sm:p-6">
        {/* Icon */}
        <div className="text-3xl sm:text-4xl mb-2 sm:mb-3">{chapter.icon}</div>

        {/* Title */}
        <h3 className="text-lg sm:text-xl font-bold text-historical-sepia dark:text-bitcoin-lightGold mb-2 sm:mb-3 group-hover:text-bitcoin-orange transition-colors duration-300 line-clamp-2">
          {chapter.title[lang]}
        </h3>

        {/* Summary - hidden on hover since it shows in overlay */}
        <p className="text-historical-antique dark:text-gray-300 text-xs sm:text-sm leading-relaxed line-clamp-2 sm:line-clamp-3 group-hover:opacity-50 transition-opacity">
          {chapter.summary[lang]}
        </p>

        {/* Read more */}
        <motion.div
          className="mt-3 sm:mt-4 flex items-center text-bitcoin-orange font-semibold text-xs sm:text-sm"
          whileHover={{ x: 5 }}
        >
          <span>{lang === 'zh' ? '阅读更多' : 'Read More'}</span>
          <svg className="w-3 h-3 sm:w-4 sm:h-4 ml-1 sm:ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </motion.div>
      </div>

      {/* Bottom accent */}
      <div className="h-1 bg-gradient-to-r from-bitcoin-orange via-bitcoin-gold to-bitcoin-darkGold group-hover:h-2 transition-all duration-300"></div>
    </motion.div>
  );
};

export default ChapterCard;
