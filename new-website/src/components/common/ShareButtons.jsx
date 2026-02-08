import { useState } from 'react';
import { FaTwitter, FaTelegramPlane, FaWeixin, FaLink, FaCheck, FaShareAlt } from 'react-icons/fa';

const ShareButtons = ({ url, title, lang = 'zh', compact = false }) => {
  const [copied, setCopied] = useState(false);
  const [showQR, setShowQR] = useState(false);

  const shareUrl = url || 'https://beihaili.github.io/Stories-about-Bitcoin/';
  const shareTitle = title || (lang === 'zh' ? '比特币那些事儿' : 'Stories about Bitcoin');

  const tweetText = lang === 'zh'
    ? `${shareTitle} - 用《明朝那些事儿》风格讲述比特币48年历史的开源双语电子书 #Bitcoin #比特币`
    : `${shareTitle} - Bitcoin's 48-year history told in web novel style. Open source & bilingual. #Bitcoin #CryptoHistory`;

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const textArea = document.createElement('textarea');
      textArea.value = shareUrl;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const buttons = [
    {
      icon: FaTwitter,
      label: 'Twitter',
      color: 'hover:bg-[#1DA1F2] hover:text-white',
      href: `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}&url=${encodeURIComponent(shareUrl)}`,
    },
    {
      icon: FaTelegramPlane,
      label: 'Telegram',
      color: 'hover:bg-[#0088cc] hover:text-white',
      href: `https://t.me/share/url?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(shareTitle)}`,
    },
  ];

  const btnSize = compact ? 'w-8 h-8 text-sm' : 'w-10 h-10 text-base';

  return (
    <div className="flex items-center gap-2">
      {buttons.map((btn) => (
        <a
          key={btn.label}
          href={btn.href}
          target="_blank"
          rel="noopener noreferrer"
          className={`${btnSize} flex items-center justify-center rounded-full bg-gray-100 text-gray-600 transition-all duration-200 ${btn.color}`}
          title={btn.label}
          onClick={(e) => e.stopPropagation()}
        >
          <btn.icon />
        </a>
      ))}

      {/* WeChat - show copy hint */}
      <div className="relative">
        <button
          className={`${btnSize} flex items-center justify-center rounded-full bg-gray-100 text-gray-600 transition-all duration-200 hover:bg-[#07C160] hover:text-white`}
          title={lang === 'zh' ? '微信分享' : 'WeChat'}
          onClick={(e) => {
            e.stopPropagation();
            setShowQR(!showQR);
            handleCopyLink();
          }}
        >
          <FaWeixin />
        </button>
        {showQR && (
          <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 bg-white rounded-lg shadow-lg p-3 text-xs text-center whitespace-nowrap z-50">
            <p className="text-gray-700 font-medium">
              {lang === 'zh' ? '链接已复制，去微信粘贴分享' : 'Link copied! Paste in WeChat'}
            </p>
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 rotate-45 w-2 h-2 bg-white"></div>
          </div>
        )}
      </div>

      {/* Copy Link */}
      <button
        className={`${btnSize} flex items-center justify-center rounded-full bg-gray-100 text-gray-600 transition-all duration-200 hover:bg-bitcoin-orange hover:text-white`}
        title={lang === 'zh' ? '复制链接' : 'Copy Link'}
        onClick={(e) => {
          e.stopPropagation();
          handleCopyLink();
        }}
      >
        {copied ? <FaCheck /> : <FaLink />}
      </button>
    </div>
  );
};

export const ShareButton = ({ url, title, lang = 'zh' }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <button
        className="w-8 h-8 flex items-center justify-center rounded-full bg-white/80 text-gray-500 hover:text-bitcoin-orange hover:bg-white transition-all duration-200 shadow-sm"
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        title={lang === 'zh' ? '分享' : 'Share'}
      >
        <FaShareAlt className="text-xs" />
      </button>
      {isOpen && (
        <div
          className="absolute top-full right-0 mt-2 bg-white rounded-xl shadow-lg p-3 z-50"
          onClick={(e) => e.stopPropagation()}
        >
          <ShareButtons url={url} title={title} lang={lang} compact />
        </div>
      )}
    </div>
  );
};

export default ShareButtons;
