import { motion } from 'framer-motion';
import { timelineEvents, categories } from '../../data/timeline';

const Timeline = ({ lang = 'zh' }) => {
  return (
    <section className="py-20 px-6 bg-gradient-to-br from-historical-sepia via-historical-antique to-historical-sepia text-white relative overflow-hidden">
      {/* Background pattern */}
      <div className="absolute inset-0 bg-book-pattern opacity-10"></div>

      <div className="max-w-6xl mx-auto relative z-10">
        {/* Section Title */}
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-5xl md:text-6xl font-bold mb-6 text-bitcoin-lightGold">
            {lang === 'zh' ? '⏳ 历史时间轴' : '⏳ Historical Timeline'}
          </h2>
          <p className="text-xl text-historical-parchment opacity-90 max-w-2xl mx-auto">
            {lang === 'zh'
              ? '从哈耶克的预言到比特币的崛起，见证货币革命的每一个里程碑'
              : 'From Hayek\'s prophecy to Bitcoin\'s rise, witness every milestone of the monetary revolution'
            }
          </p>
        </motion.div>

        {/* Timeline */}
        <div className="relative" role="list" aria-label={lang === 'zh' ? '历史事件列表' : 'Historical events list'}>
          {/* Center line */}
          <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-bitcoin-gold via-bitcoin-orange to-bitcoin-darkGold opacity-30 hidden md:block" aria-hidden="true"></div>
          {/* Mobile left line */}
          <div className="absolute left-4 w-1 h-full bg-gradient-to-b from-bitcoin-gold via-bitcoin-orange to-bitcoin-darkGold opacity-30 md:hidden" aria-hidden="true"></div>

          {/* Events */}
          {timelineEvents.map((event, index) => {
            const isLeft = index % 2 === 0;

            return (
              <motion.div
                key={index}
                role="listitem"
                className={`relative mb-12 flex items-center ${
                  isLeft ? 'md:justify-start' : 'md:justify-end'
                } justify-start`}
                initial={{ opacity: 0, x: isLeft ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
              >
                {/* Content */}
                <motion.div
                  className={`w-[calc(100%-2.5rem)] ml-10 md:ml-0 md:w-5/12 ${
                    isLeft ? 'md:text-right md:pr-12' : 'md:text-left md:pl-12'
                  } text-left pl-0`}
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="bg-black bg-opacity-70 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-xl border-2 border-bitcoin-gold border-opacity-50 hover:border-opacity-100 transition-all duration-300">
                    {/* Date */}
                    <div className="text-bitcoin-gold font-bold text-lg md:text-xl mb-2 md:mb-3">
                      {event.date}
                    </div>

                    {/* Title */}
                    <h3 className="text-lg md:text-2xl font-bold mb-2 md:mb-4 text-white">
                      {event.title[lang]}
                    </h3>

                    {/* Description */}
                    <p className="text-sm md:text-base text-white leading-relaxed">
                      {event.description[lang]}
                    </p>

                    {/* Category badge */}
                    <div className="mt-3 md:mt-4 inline-block">
                      <span
                        className="px-3 md:px-4 py-1 md:py-2 rounded-full text-xs md:text-sm font-semibold bg-white bg-opacity-20 text-white border border-white border-opacity-30"
                      >
                        {categories[event.category]?.[lang]}
                      </span>
                    </div>
                  </div>
                </motion.div>

                {/* Timeline dot */}
                <motion.div
                  className="absolute left-4 md:left-1/2 transform -translate-x-1/2"
                  whileHover={{ scale: 1.5 }}
                >
                  <div
                    className={`rounded-full shadow-lg ${
                      event.importance === 'critical'
                        ? 'w-4 h-4 md:w-6 md:h-6 bg-bitcoin-orange'
                        : event.importance === 'high'
                        ? 'w-3.5 h-3.5 md:w-5 md:h-5 bg-bitcoin-gold'
                        : 'w-3 h-3 md:w-4 md:h-4 bg-bitcoin-darkGold'
                    }`}
                    style={{
                      boxShadow: `0 0 20px ${categories[event.category]?.color}`,
                    }}
                  ></div>
                </motion.div>
              </motion.div>
            );
          })}
        </div>

        {/* Legend */}
        <motion.div
          className="mt-16 flex flex-wrap justify-center gap-6"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-full bg-bitcoin-orange"></div>
            <span className="text-sm text-bitcoin-lightGold">
              {lang === 'zh' ? '关键事件' : 'Critical'}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 rounded-full bg-bitcoin-gold"></div>
            <span className="text-sm text-bitcoin-lightGold">
              {lang === 'zh' ? '重要事件' : 'High'}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-bitcoin-darkGold"></div>
            <span className="text-sm text-bitcoin-lightGold">
              {lang === 'zh' ? '一般事件' : 'Medium'}
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Timeline;
