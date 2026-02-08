import { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaQuoteLeft, FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import { figures } from '../../data/figures';

const FiguresGallery = ({ lang = 'zh' }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextFigure = useCallback(() => {
    setCurrentIndex((prev) => (prev + 1) % figures.length);
  }, []);

  const prevFigure = useCallback(() => {
    setCurrentIndex((prev) => (prev - 1 + figures.length) % figures.length);
  }, []);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      const gallery = document.getElementById('figures');
      if (!gallery) return;
      const rect = gallery.getBoundingClientRect();
      const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
      if (!isVisible) return;

      if (e.key === 'ArrowLeft') {
        prevFigure();
      } else if (e.key === 'ArrowRight') {
        nextFigure();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [nextFigure, prevFigure]);

  const currentFigure = figures[currentIndex];

  return (
    <section className="py-20 px-6 bg-gradient-to-br from-bitcoin-lightGold via-white to-historical-parchment" aria-label={lang === 'zh' ? '关键人物展示' : 'Key Figures Gallery'}>
      <div className="max-w-6xl mx-auto">
        {/* Section Title */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="section-title">
            {lang === 'zh' ? '👥 关键人物' : '👥 Key Figures'}
          </h2>
          <p className="text-xl text-historical-antique max-w-2xl mx-auto">
            {lang === 'zh'
              ? '认识这场货币革命背后的先驱者和传奇人物'
              : 'Meet the pioneers and legends behind this monetary revolution'
            }
          </p>
        </motion.div>

        {/* Gallery */}
        <div className="relative" aria-live="polite" aria-atomic="true">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentIndex}
              initial={{ opacity: 0, x: 100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -100 }}
              transition={{ duration: 0.5 }}
              className="bg-white rounded-2xl shadow-book overflow-hidden"
            >
              <div className="grid md:grid-cols-2 gap-8 p-8">
                {/* Left: Image & Basic Info */}
                <div className="text-center md:text-left">
                  {/* Portrait placeholder */}
                  <motion.div
                    className="w-64 h-64 mx-auto md:mx-0 mb-6 rounded-full bg-gradient-to-br from-bitcoin-orange to-bitcoin-gold flex items-center justify-center text-9xl shadow-2xl"
                    whileHover={{ scale: 1.05, rotate: 5 }}
                  >
                    {currentFigure.id === 'satoshi' ? '🎭' :
                     currentFigure.id === 'hayek' ? '📖' :
                     currentFigure.id === 'hal-finney' ? '💻' :
                     currentFigure.id === 'chaum' ? '🔐' : '👤'}
                  </motion.div>

                  {/* Name */}
                  <h3 className="text-3xl font-bold text-historical-sepia mb-2">
                    {currentFigure.name[lang]}
                  </h3>

                  {/* Role */}
                  <p className="text-lg text-bitcoin-orange font-semibold mb-2">
                    {currentFigure.role[lang]}
                  </p>

                  {/* Years */}
                  <p className="text-historical-antique mb-6">
                    {currentFigure.years}
                  </p>

                  {/* Quote */}
                  <div className="bg-historical-parchment p-6 rounded-xl relative">
                    <FaQuoteLeft className="text-bitcoin-orange opacity-30 text-3xl absolute top-4 left-4" />
                    <p className="text-historical-sepia italic pt-8 leading-relaxed text-sm">
                      "{currentFigure.quote[lang]}"
                    </p>
                  </div>
                </div>

                {/* Right: Details */}
                <div>
                  {/* Description */}
                  <div className="mb-6">
                    <h4 className="text-xl font-bold text-historical-sepia mb-3 flex items-center gap-2">
                      <span className="text-2xl">📜</span>
                      {lang === 'zh' ? '简介' : 'Biography'}
                    </h4>
                    <p className="text-historical-antique leading-relaxed">
                      {currentFigure.description[lang]}
                    </p>
                  </div>

                  {/* Contributions */}
                  <div>
                    <h4 className="text-xl font-bold text-historical-sepia mb-3 flex items-center gap-2">
                      <span className="text-2xl">🌟</span>
                      {lang === 'zh' ? '主要贡献' : 'Key Contributions'}
                    </h4>
                    <ul className="space-y-2">
                      {currentFigure.contributions[lang].map((contribution, idx) => (
                        <motion.li
                          key={idx}
                          className="flex items-start gap-3 text-historical-antique"
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.1 }}
                        >
                          <span className="text-bitcoin-orange text-xl flex-shrink-0">•</span>
                          <span>{contribution}</span>
                        </motion.li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </motion.div>
          </AnimatePresence>

          {/* Navigation Buttons */}
          <button
            onClick={prevFigure}
            aria-label={lang === 'zh' ? '上一位人物' : 'Previous figure'}
            className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-1/2 bg-white hover:bg-bitcoin-orange text-historical-sepia hover:text-white rounded-full p-4 shadow-lg transition-all duration-300 z-10 focus-ring"
          >
            <FaChevronLeft className="text-xl" />
          </button>
          <button
            onClick={nextFigure}
            aria-label={lang === 'zh' ? '下一位人物' : 'Next figure'}
            className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1/2 bg-white hover:bg-bitcoin-orange text-historical-sepia hover:text-white rounded-full p-4 shadow-lg transition-all duration-300 z-10 focus-ring"
          >
            <FaChevronRight className="text-xl" />
          </button>
        </div>

        {/* Indicators */}
        <div className="flex justify-center gap-3 mt-8" role="tablist" aria-label={lang === 'zh' ? '人物选择' : 'Figure selection'}>
          {figures.map((figure, idx) => (
            <button
              key={idx}
              role="tab"
              aria-selected={idx === currentIndex}
              aria-label={figure.name[lang]}
              onClick={() => setCurrentIndex(idx)}
              className={`w-3 h-3 rounded-full transition-all duration-300 focus-ring ${
                idx === currentIndex
                  ? 'bg-bitcoin-orange w-8'
                  : 'bg-gray-300 hover:bg-gray-400'
              }`}
            />
          ))}
        </div>

        {/* Counter */}
        <p className="text-center mt-6 text-historical-antique">
          {currentIndex + 1} / {figures.length}
        </p>
      </div>
    </section>
  );
};

export default FiguresGallery;
