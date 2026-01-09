import { useState } from 'react';
import { motion } from 'framer-motion';
import ChapterCard from './ChapterCard';
import { chapters, periods, getChaptersByPeriod } from '../../data/chapters';

const ChapterGrid = ({ lang = 'zh' }) => {
  const [selectedPeriod, setSelectedPeriod] = useState('all');

  const filteredChapters = selectedPeriod === 'all'
    ? chapters
    : getChaptersByPeriod(selectedPeriod);

  return (
    <section className="py-20 px-6 bg-warm-gradient">
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
          <p className="text-xl text-historical-antique max-w-2xl mx-auto">
            {lang === 'zh'
              ? '穿越48年时光，重访比特币诞生前后的关键历史时刻'
              : 'Travel through 48 years to revisit key historical moments before and after Bitcoin\'s birth'
            }
          </p>
        </motion.div>

        {/* Period Filter */}
        <motion.div
          className="flex flex-wrap justify-center gap-3 mb-12"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <button
            onClick={() => setSelectedPeriod('all')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
              selectedPeriod === 'all'
                ? 'bg-bitcoin-orange text-white shadow-lg scale-105'
                : 'bg-white text-historical-sepia hover:bg-gray-50 shadow'
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
                  : 'bg-white text-historical-sepia hover:bg-gray-50 shadow'
              }`}
            >
              {period.name[lang]}
              {period.years && <span className="ml-2 text-sm opacity-75">({period.years})</span>}
            </button>
          ))}
        </motion.div>

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
            />
          ))}
        </motion.div>

        {/* Stats */}
        <motion.div
          className="mt-16 text-center"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <p className="text-lg text-historical-antique">
            {lang === 'zh'
              ? `共 ${filteredChapters.length} 章${selectedPeriod !== 'all' ? ` · ${periods.find(p => p.id === selectedPeriod)?.name[lang]}` : ''}`
              : `${filteredChapters.length} Chapters${selectedPeriod !== 'all' ? ` · ${periods.find(p => p.id === selectedPeriod)?.name[lang]}` : ''}`
            }
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default ChapterGrid;
