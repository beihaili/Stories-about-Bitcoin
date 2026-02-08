import { Component } from 'react';

const messages = {
  zh: {
    title: '加载出错了',
    description: '这个部分暂时无法显示，请刷新页面重试。',
    retry: '刷新页面',
  },
  en: {
    title: 'Something went wrong',
    description: 'This section could not be loaded. Please refresh the page to try again.',
    retry: 'Refresh page',
  },
};

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      const lang = this.props.lang || 'zh';
      const t = messages[lang];
      return (
        <div className="py-16 text-center px-4">
          <h3 className="text-2xl font-bold text-historical-sepia dark:text-bitcoin-lightGold mb-3">
            {t.title}
          </h3>
          <p className="text-historical-antique dark:text-gray-300 mb-6">
            {t.description}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="btn-primary text-sm px-6 py-2"
          >
            {t.retry}
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
