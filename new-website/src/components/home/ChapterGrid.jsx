import { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import ChapterCard from './ChapterCard';
import { chapters, periods, getChaptersByPeriod } from '../../data/chapters';

const ChapterGrid = ({
  lang = 'zh',
  markAsRead,
  isRead,
  readCount = 0,
  unlockedCount = 0,
  totalAchievements = 0,
  isPeriodComplete,
  isBookmarked,
  toggleBookmark,
}) => {
  const [selectedPeriod, setSelectedPeriod] = useState('all');
  const [filter, setFilter] = useState('all'); // 'all' | 'bookmarked' | 'unread'

  const filteredChapters = useMemo(() => {
    let result = selectedPeriod === 'all' ? chapters : getChaptersByPeriod(selectedPeriod);
    if (filter === 'bookmarked') {
      result = result.filter(ch => isBookmarked?.(ch.id));
    } else if (filter === 'unread') {
      result = result.filter(ch => !isRead?.(ch.id));
    }
    return result;
  }, [selectedPeriod, filter, isRead, isBookmarked]);

  const percentage = Math.round((readCount / chapters.length) * 100);

  return (
    <section className="py-20 px-6 bg-warm-gradient dark:bg-gray-900">
      <div className="max-w-7xl mx-auto">
        {/* Section Title */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="section-title">
            {lang === 'zh' ? '📚 章节目录' : '📚 Chapters'}
          </h2>
          <p className="text-xl text-historical-antique dark:text-gray-300 max-w-2xl mx-auto">
            {lang === 'zh'
              ? '穿越48年时光，重访比特币诞生前后的关键历史时刻'
              : 'Travel through 48 years to revisit key historical moments before and after Bitcoin\'s birth'
            }
          </p>
        </motion.div>

        {/* Reading Stats Panel */}
        {readCount > 0 && (
          <motion.div
            className="mb-12 bg-gradient-to-r from-bitcoin-orange/10 to-bitcoin-gold/10 dark:from-bitcoin-orange/20 dark:to-bitcoin-gold/20 rounded-2xl p-6 border border-bitcoin-orange/20"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-bitcoin-orange">{readCount}/{chapters.length}</div>
                <div className="text-xs text-historical-antique dark:text-gray-400">{lang === 'zh' ? '已读章节' : 'Chapters Read'}</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-bitcoin-orange">{percentage}%</div>
                <div className="text-xs text-historical-antique dark:text-gray-400">{lang === 'zh' ? '完成进度' : 'Progress'}</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-bitcoin-orange">{unlockedCount}/{totalAchievements}</div>
                <div className="text-xs text-historical-antique dark:text-gray-400">{lang === 'zh' ? '成就解锁' : 'Achievements'}</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-bitcoin-orange">
                  {chapters.reduce((sum, ch) => isRead?.(ch.id) ? sum + (ch.readingTime || 0) : sum, 0)}
                </div>
                <div className="text-xs text-historical-antique dark:text-gray-400">{lang === 'zh' ? '阅读分钟' : 'Min Read'}</div>
              </div>
            </div>
            {/* Progress Bar */}
            <div className="mt-4 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-bitcoin-orange to-bitcoin-gold rounded-full"
                initial={{ width: 0 }}
                whileInView={{ width: `${percentage}%` }}
                viewport={{ once: true }}
                transition={{ duration: 1, ease: 'easeOut' }}
              />
            </div>
          </motion.div>
        )}

        {/* Period Filter */}
        <motion.div
          className="flex flex-wrap justify-center gap-3 mb-6"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <button
            onClick={() => setSelectedPeriod('all')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
              selectedPeriod === 'all'
                ? 'bg-bitcoin-orange text-white shadow-lg scale-105'
                : 'bg-white dark:bg-gray-800 text-historical-sepia dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 shadow'
            }`}
          >
            {lang === 'zh' ? '全部' : 'All'}
          </button>
          {periods.map((period) => (
            <button
              key={period.id}
              onClick={() => setSelectedPeriod(period.id)}
              className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
                selectedPeriod === period.id
                  ? 'bg-bitcoin-orange text-white shadow-lg scale-105'
                  : 'bg-white dark:bg-gray-800 text-historical-sepia dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 shadow'
              }`}
            >
              {period.name[lang]}
              {period.years && <span className="ml-2 text-sm opacity-75">({period.years})</span>}
              {isPeriodComplete?.(period.id) && <span className="ml-1">✓</span>}
            </button>
          ))}
        </motion.div>

        {/* Filter Tags */}
        <div className="flex justify-center gap-2 mb-12">
          {['all', 'bookmarked', 'unread'].map((f) => {
            const labels = {
              all: { zh: '全部', en: 'All' },
              bookmarked: { zh: '收藏', en: 'Bookmarked' },
              unread: { zh: '未读', en: 'Unread' },
            };
            return (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                  filter === f
                    ? 'bg-bitcoin-orange text-white'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                }`}
              >
                {labels[f][lang]}
              </button>
            );
          })}
        </div>

        {/* Chapters Grid */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
          layout
        >
          {filteredChapters.map((chapter, index) => (
            <ChapterCard
              key={chapter.id}
              chapter={chapter}
              lang={lang}
              index={index}
              markAsRead={markAsRead}
              isRead={isRead?.(chapter.id)}
              isBookmarked={isBookmarked?.(chapter.id)}
              toggleBookmark={toggleBookmark}
            />
          ))}
        </motion.div>

        {/* Empty State */}
        {filteredChapters.length === 0 && (
          <div className="text-center py-12">
            <p className="text-lg text-historical-antique dark:text-gray-400">
              {filter === 'bookmarked'
                ? (lang === 'zh' ? '还没有收藏的章节' : 'No bookmarked chapters yet')
                : (lang === 'zh' ? '全部读完了！' : 'All chapters read!')
              }
            </p>
          </div>
        )}

        {/* Stats */}
        <motion.div
          className="mt-16 text-center"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <p className="text-lg text-historical-antique dark:text-gray-400">
            {lang === 'zh'
              ? `共 ${filteredChapters.length} 章${selectedPeriod !== 'all' ? ` · ${periods.find(p => p.id === selectedPeriod)?.name[lang]}` : ''}`
              : `${filteredChapters.length} Chapters${selectedPeriod !== 'all' ? ` · ${periods.find(p => p.id === selectedPeriod)?.name[lang]}` : ''}`
            }
          </p>
          {readCount > 0 && (
            <p className="text-sm text-bitcoin-orange mt-2">
              {lang === 'zh'
                ? `已读 ${readCount}/${chapters.length} 章`
                : `${readCount}/${chapters.length} chapters read`
              }
            </p>
          )}
        </motion.div>
      </div>
    </section>
  );
};

export default ChapterGrid;
