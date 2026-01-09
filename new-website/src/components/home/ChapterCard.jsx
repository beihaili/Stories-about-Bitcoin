import { motion } from 'framer-motion';

const ChapterCard = ({ chapter, lang = 'zh', index }) => {
  const handleClick = () => {
    // 跳转到 GitBook 章节页面
    const baseUrl = 'https://beihaili.github.io/Stories-about-Bitcoin';
    window.open(`${baseUrl}${chapter.link[lang]}`, '_blank');
  };

  return (
    <motion.div
      className="chapter-card group"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      whileHover={{ y: -8 }}
      onClick={handleClick}
    >
      {/* Image */}
      <div className="relative h-56 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-bitcoin-orange to-bitcoin-gold opacity-80 group-hover:opacity-90 transition-opacity duration-300"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-8xl opacity-30">{chapter.icon}</span>
        </div>
        {/* Period label */}
        <div className="absolute top-4 left-4 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-semibold text-historical-sepia">
          {chapter.year || lang === 'zh' ? '序言' : 'Prologue'}
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Icon */}
        <div className="text-4xl mb-3">{chapter.icon}</div>

        {/* Title */}
        <h3 className="text-xl font-bold text-historical-sepia mb-3 group-hover:text-bitcoin-orange transition-colors duration-300 line-clamp-2">
          {chapter.title[lang]}
        </h3>

        {/* Summary */}
        <p className="text-historical-antique text-sm leading-relaxed line-clamp-3">
          {chapter.summary[lang]}
        </p>

        {/* Read more */}
        <motion.div
          className="mt-4 flex items-center text-bitcoin-orange font-semibold text-sm"
          whileHover={{ x: 5 }}
        >
          <span>{lang === 'zh' ? '阅读更多' : 'Read More'}</span>
          <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
