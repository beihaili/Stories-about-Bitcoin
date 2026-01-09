import { motion } from 'framer-motion';
import { FaBook, FaGithub, FaDownload } from 'react-icons/fa';

const Hero = ({ lang = 'zh' }) => {
  const content = {
    zh: {
      title: '比特币那些事儿',
      subtitle: '以网文笔法讲比特币的故事',
      description: '用轻松有趣的方式，带你了解从1976年哈耶克的货币理论到2024年比特币发展的历史故事',
      cta: '开始阅读',
      github: 'GitHub',
      download: '下载PDF'
    },
    en: {
      title: 'Stories about Bitcoin',
      subtitle: 'Bitcoin Stories in Web Novel Style',
      description: 'An engaging journey through Bitcoin\'s history, from Hayek\'s monetary theory in 1976 to Bitcoin\'s evolution in 2024',
      cta: 'Start Reading',
      github: 'GitHub',
      download: 'Download PDF'
    }
  };

  const t = content[lang];

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-historical-parchment via-bitcoin-lightGold to-historical-parchment">
      {/* Background pattern */}
      <div className="absolute inset-0 bg-book-pattern opacity-30"></div>

      {/* Animated circles */}
      <motion.div
        className="absolute top-20 left-20 w-64 h-64 bg-bitcoin-gold opacity-10 rounded-full blur-3xl"
        animate={{
          scale: [1, 1.2, 1],
          x: [0, 50, 0],
          y: [0, 30, 0]
        }}
        transition={{ duration: 20, repeat: Infinity }}
      />
      <motion.div
        className="absolute bottom-20 right-20 w-96 h-96 bg-bitcoin-orange opacity-10 rounded-full blur-3xl"
        animate={{
          scale: [1, 1.3, 1],
          x: [0, -50, 0],
          y: [0, -30, 0]
        }}
        transition={{ duration: 25, repeat: Infinity }}
      />

      {/* Content */}
      <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          {/* Icon */}
          <motion.div
            className="inline-block mb-8"
            animate={{ rotateY: [0, 360] }}
            transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
          >
            <FaBook className="text-7xl text-bitcoin-orange drop-shadow-lg" />
          </motion.div>

          {/* Title */}
          <h1 className="text-6xl md:text-8xl font-bold text-historical-sepia mb-4 tracking-tight">
            {t.title}
          </h1>

          {/* Subtitle */}
          <p className="text-2xl md:text-3xl text-bitcoin-darkGold font-semibold mb-6">
            {t.subtitle}
          </p>

          {/* Description */}
          <p className="text-lg md:text-xl text-historical-antique max-w-3xl mx-auto mb-12 leading-relaxed">
            {t.description}
          </p>

          {/* Stats */}
          <motion.div
            className="flex justify-center gap-8 mb-12 flex-wrap"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <div className="text-center">
              <div className="text-4xl font-bold text-bitcoin-orange">33</div>
              <div className="text-sm text-historical-antique">{lang === 'zh' ? '章节' : 'Chapters'}</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-bitcoin-orange">1976-2024</div>
              <div className="text-sm text-historical-antique">{lang === 'zh' ? '跨越48年' : '48 Years'}</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-bitcoin-orange">7</div>
              <div className="text-sm text-historical-antique">{lang === 'zh' ? '历史时期' : 'Periods'}</div>
            </div>
          </motion.div>

          {/* CTA Buttons */}
          <motion.div
            className="flex justify-center gap-6 flex-wrap"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
          >
            <a
              href={`https://beihaili.github.io/Stories-about-Bitcoin/${lang}/`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary text-lg px-8 py-4 flex items-center gap-3"
            >
              <FaBook />
              {t.cta}
            </a>
            <a
              href="https://github.com/beihaili/Stories-about-Bitcoin"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gray-800 hover:bg-gray-700 text-white font-semibold py-4 px-8 rounded-lg shadow-lg transition-all duration-300 flex items-center gap-3"
            >
              <FaGithub />
              {t.github}
            </a>
            <a
              href="https://github.com/beihaili/Stories-about-Bitcoin/releases"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white hover:bg-gray-50 text-historical-sepia font-semibold py-4 px-8 rounded-lg shadow-lg transition-all duration-300 border-2 border-bitcoin-orange flex items-center gap-3"
            >
              <FaDownload />
              {t.download}
            </a>
          </motion.div>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="w-6 h-10 border-2 border-bitcoin-orange rounded-full flex justify-center">
            <motion.div
              className="w-2 h-2 bg-bitcoin-orange rounded-full mt-2"
              animate={{ y: [0, 16, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;
