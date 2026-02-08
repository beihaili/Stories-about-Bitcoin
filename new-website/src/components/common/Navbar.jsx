import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaBook, FaGithub, FaBars, FaTimes } from 'react-icons/fa';
import LanguageSwitcher from './LanguageSwitcher';

const Navbar = ({ lang, setLang }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const content = {
    zh: {
      title: '比特币那些事儿',
      read: '开始阅读',
      chapters: '章节目录',
      timeline: '时间线',
      figures: '关键人物',
    },
    en: {
      title: 'Stories about Bitcoin',
      read: 'Start Reading',
      chapters: 'Chapters',
      timeline: 'Timeline',
      figures: 'Key Figures',
    }
  };

  const t = content[lang];

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMobileMenuOpen(false);
  };

  return (
    <>
      <motion.nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          isScrolled
            ? 'bg-white/95 backdrop-blur-md shadow-lg'
            : 'bg-transparent'
        }`}
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16 sm:h-20">
            {/* Logo */}
            <motion.a
              href="#"
              className="flex items-center gap-2 sm:gap-3"
              whileHover={{ scale: 1.02 }}
              onClick={(e) => {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
            >
              <FaBook className={`text-xl sm:text-2xl ${isScrolled ? 'text-bitcoin-orange' : 'text-bitcoin-orange'}`} />
              <span className={`font-bold text-base sm:text-lg ${isScrolled ? 'text-historical-sepia' : 'text-historical-sepia'}`}>
                {t.title}
              </span>
            </motion.a>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-6 lg:gap-8">
              <button
                onClick={() => scrollToSection('timeline')}
                className={`font-medium transition-colors ${
                  isScrolled ? 'text-historical-antique hover:text-bitcoin-orange' : 'text-historical-sepia hover:text-bitcoin-orange'
                }`}
              >
                {t.timeline}
              </button>
              <button
                onClick={() => scrollToSection('figures')}
                className={`font-medium transition-colors ${
                  isScrolled ? 'text-historical-antique hover:text-bitcoin-orange' : 'text-historical-sepia hover:text-bitcoin-orange'
                }`}
              >
                {t.figures}
              </button>
              <button
                onClick={() => scrollToSection('chapters')}
                className={`font-medium transition-colors ${
                  isScrolled ? 'text-historical-antique hover:text-bitcoin-orange' : 'text-historical-sepia hover:text-bitcoin-orange'
                }`}
              >
                {t.chapters}
              </button>

              <a
                href="https://github.com/beihaili/Stories-about-Bitcoin"
                target="_blank"
                rel="noopener noreferrer"
                className={`transition-colors ${
                  isScrolled ? 'text-historical-antique hover:text-bitcoin-orange' : 'text-historical-sepia hover:text-bitcoin-orange'
                }`}
              >
                <FaGithub className="text-xl" />
              </a>

              <LanguageSwitcher lang={lang} setLang={setLang} isCompact />

              <a
                href={`https://beihaili.github.io/Stories-about-Bitcoin/${lang}/`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary text-sm px-4 py-2"
              >
                {t.read}
              </a>
            </div>

            {/* Mobile Menu Button */}
            <div className="flex items-center gap-3 md:hidden">
              <LanguageSwitcher lang={lang} setLang={setLang} isCompact />
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="p-2 text-historical-sepia"
              >
                {isMobileMenuOpen ? <FaTimes className="text-xl" /> : <FaBars className="text-xl" />}
              </button>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            className="fixed inset-0 z-40 bg-white md:hidden"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
          >
            <div className="flex flex-col items-center justify-center h-full gap-6 pt-20">
              <button
                onClick={() => scrollToSection('timeline')}
                className="text-xl font-medium text-historical-sepia hover:text-bitcoin-orange transition-colors"
              >
                {t.timeline}
              </button>
              <button
                onClick={() => scrollToSection('figures')}
                className="text-xl font-medium text-historical-sepia hover:text-bitcoin-orange transition-colors"
              >
                {t.figures}
              </button>
              <button
                onClick={() => scrollToSection('chapters')}
                className="text-xl font-medium text-historical-sepia hover:text-bitcoin-orange transition-colors"
              >
                {t.chapters}
              </button>
              <a
                href="https://github.com/beihaili/Stories-about-Bitcoin"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-xl font-medium text-historical-sepia hover:text-bitcoin-orange transition-colors"
              >
                <FaGithub />
                GitHub
              </a>
              <a
                href={`https://beihaili.github.io/Stories-about-Bitcoin/${lang}/`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary text-lg px-8 py-3 mt-4"
              >
                {t.read}
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default Navbar;
