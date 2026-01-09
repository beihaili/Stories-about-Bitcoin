import { motion } from 'framer-motion';

const LanguageSwitcher = ({ lang, setLang }) => {
  return (
    <motion.div
      className="fixed top-6 right-6 z-50 flex gap-2 bg-white rounded-full shadow-lg p-2"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5 }}
    >
      <button
        onClick={() => setLang('zh')}
        className={`px-4 py-2 rounded-full font-semibold transition-all duration-300 ${
          lang === 'zh'
            ? 'bg-bitcoin-orange text-white shadow-md'
            : 'text-historical-sepia hover:bg-gray-100'
        }`}
      >
        中文
      </button>
      <button
        onClick={() => setLang('en')}
        className={`px-4 py-2 rounded-full font-semibold transition-all duration-300 ${
          lang === 'en'
            ? 'bg-bitcoin-orange text-white shadow-md'
            : 'text-historical-sepia hover:bg-gray-100'
        }`}
      >
        English
      </button>
    </motion.div>
  );
};

export default LanguageSwitcher;
