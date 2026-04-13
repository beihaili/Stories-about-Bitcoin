import { render, screen, act, cleanup } from '@testing-library/react'
import TypewriterQuotes from '../TypewriterQuotes'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

describe('TypewriterQuotes', () => {
  let observerInstances

  beforeEach(() => {
    observerInstances = []
    global.IntersectionObserver = vi.fn(function (callback, options) {
      const instance = {
        callback,
        options,
        observe: vi.fn(),
        unobserve: vi.fn(),
        disconnect: vi.fn(),
      }
      observerInstances.push(instance)
      return instance
    })
  })

  afterEach(() => {
    cleanup()
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  describe('rendering', () => {
    it('renders the container wrapper with layout classes', () => {
      const { container } = render(<TypewriterQuotes />)
      const wrapper = container.firstChild
      expect(wrapper).toBeInTheDocument()
      expect(wrapper.className).toContain('min-h-')
      expect(wrapper.className).toContain('flex')
    })

    it('defaults to Chinese quotes when no lang prop is provided', () => {
      render(<TypewriterQuotes />)
      expect(screen.getByText(/中本聪 · 创世区块/)).toBeInTheDocument()
    })

    it('renders Chinese author when lang="zh"', () => {
      render(<TypewriterQuotes lang="zh" />)
      expect(screen.getByText(/中本聪 · 创世区块/)).toBeInTheDocument()
    })

    it('renders English author when lang="en"', () => {
      render(<TypewriterQuotes lang="en" />)
      expect(screen.getByText(/Satoshi Nakamoto · Genesis Block/)).toBeInTheDocument()
    })

    it('prefixes the author with an em-dash', () => {
      render(<TypewriterQuotes lang="zh" />)
      expect(screen.getByText(/^— /)).toBeInTheDocument()
    })

    it('starts with empty displayed text before any timer fires', () => {
      vi.useFakeTimers()
      const { container } = render(<TypewriterQuotes />)
      const textSpan = container.querySelector('span')
      expect(textSpan.textContent).toBe('')
    })

    it('renders the blinking cursor element', () => {
      const { container } = render(<TypewriterQuotes />)
      const cursor = container.querySelector('.bg-bitcoin-orange')
      expect(cursor).toBeInTheDocument()
    })

    it('applies typographic classes to the quote text', () => {
      const { container } = render(<TypewriterQuotes />)
      const quoteBlock = container.querySelector('.font-serif')
      expect(quoteBlock).toBeInTheDocument()
      expect(quoteBlock.className).toContain('italic')
    })
  })

  describe('IntersectionObserver integration', () => {
    it('creates an IntersectionObserver with threshold 0 and 100px rootMargin', () => {
      render(<TypewriterQuotes />)
      expect(global.IntersectionObserver).toHaveBeenCalledTimes(1)
      const [, options] = global.IntersectionObserver.mock.calls[0]
      expect(options).toEqual({ threshold: 0, rootMargin: '100px' })
    })

    it('observes the container wrapper element', () => {
      const { container } = render(<TypewriterQuotes />)
      expect(observerInstances).toHaveLength(1)
      expect(observerInstances[0].observe).toHaveBeenCalledWith(container.firstChild)
    })

    it('disconnects the observer on unmount', () => {
      const { unmount } = render(<TypewriterQuotes />)
      unmount()
      expect(observerInstances[0].disconnect).toHaveBeenCalled()
    })
  })

  describe('typing animation', () => {
    it('begins typing characters after the initial tick timeout', () => {
      vi.useFakeTimers()
      const { container } = render(<TypewriterQuotes />)
      act(() => {
        vi.advanceTimersByTime(60)
      })
      const textSpan = container.querySelector('span')
      expect(textSpan.textContent.length).toBeGreaterThan(0)
    })

    it('progressively types more characters as time advances', () => {
      vi.useFakeTimers()
      const { container } = render(<TypewriterQuotes />)
      act(() => {
        vi.advanceTimersByTime(60)
      })
      const firstLen = container.querySelector('span').textContent.length

      act(() => {
        vi.advanceTimersByTime(300)
      })
      const laterLen = container.querySelector('span').textContent.length

      expect(laterLen).toBeGreaterThan(firstLen)
    })

    it('types a prefix of the current quote text', () => {
      vi.useFakeTimers()
      const { container } = render(<TypewriterQuotes lang="en" />)
      act(() => {
        vi.advanceTimersByTime(500)
      })
      const typed = container.querySelector('span').textContent
      const fullQuote = '"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"'
      expect(fullQuote.startsWith(typed)).toBe(true)
    })
  })

  describe('offscreen pause behavior', () => {
    it('stops advancing displayed text when the observer reports not intersecting', () => {
      vi.useFakeTimers()
      const { container } = render(<TypewriterQuotes />)

      act(() => {
        observerInstances[0].callback([{ isIntersecting: false }])
      })
      act(() => {
        vi.advanceTimersByTime(100)
      })
      const baseline = container.querySelector('span').textContent.length

      act(() => {
        vi.advanceTimersByTime(1000)
      })
      const afterWait = container.querySelector('span').textContent.length

      expect(afterWait).toBe(baseline)
    })

    it('resumes typing after visibility returns', () => {
      vi.useFakeTimers()
      const { container } = render(<TypewriterQuotes />)

      act(() => {
        observerInstances[0].callback([{ isIntersecting: false }])
        vi.advanceTimersByTime(500)
      })
      const pausedLen = container.querySelector('span').textContent.length

      act(() => {
        observerInstances[0].callback([{ isIntersecting: true }])
        vi.advanceTimersByTime(500)
      })
      const resumedLen = container.querySelector('span').textContent.length

      expect(resumedLen).toBeGreaterThan(pausedLen)
    })
  })

  describe('lang prop changes', () => {
    it('switches to English author when lang changes from zh to en', () => {
      const { rerender } = render(<TypewriterQuotes lang="zh" />)
      expect(screen.getByText(/中本聪 · 创世区块/)).toBeInTheDocument()

      rerender(<TypewriterQuotes lang="en" />)
      expect(screen.getByText(/Satoshi Nakamoto · Genesis Block/)).toBeInTheDocument()
    })

    it('switches to Chinese author when lang changes from en to zh', () => {
      const { rerender } = render(<TypewriterQuotes lang="en" />)
      expect(screen.getByText(/Satoshi Nakamoto · Genesis Block/)).toBeInTheDocument()

      rerender(<TypewriterQuotes lang="zh" />)
      expect(screen.getByText(/中本聪 · 创世区块/)).toBeInTheDocument()
    })
  })

  describe('edge cases', () => {
    it('does not throw when rendering and unmounting immediately', () => {
      expect(() => {
        const { unmount } = render(<TypewriterQuotes />)
        unmount()
      }).not.toThrow()
    })

    it('does not leave pending timers that update state after unmount', () => {
      vi.useFakeTimers()
      const { unmount } = render(<TypewriterQuotes />)
      unmount()
      expect(() => {
        act(() => {
          vi.advanceTimersByTime(5000)
        })
      }).not.toThrow()
    })

    it('supports mounting multiple instances independently', () => {
      const first = render(<TypewriterQuotes lang="zh" />)
      const second = render(<TypewriterQuotes lang="en" />)

      expect(observerInstances).toHaveLength(2)
      expect(first.container.firstChild).toBeInTheDocument()
      expect(second.container.firstChild).toBeInTheDocument()

      first.unmount()
      second.unmount()
    })

    it('handles an immediate visibility toggle without crashing', () => {
      vi.useFakeTimers()
      render(<TypewriterQuotes />)

      expect(() => {
        act(() => {
          observerInstances[0].callback([{ isIntersecting: false }])
          observerInstances[0].callback([{ isIntersecting: true }])
          observerInstances[0].callback([{ isIntersecting: false }])
          vi.advanceTimersByTime(300)
        })
      }).not.toThrow()
    })
  })
})
