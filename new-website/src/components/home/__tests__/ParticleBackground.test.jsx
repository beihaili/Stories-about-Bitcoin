import { render, cleanup } from '@testing-library/react'
import ParticleBackground from '../ParticleBackground'

describe('ParticleBackground', () => {
  let ctxMock
  let observerInstances
  let rafCallbacks
  let rafId
  let originalRAF
  let originalCAF
  let originalInnerWidth
  let originalInnerHeight

  beforeEach(() => {
    ctxMock = {
      fillRect: vi.fn(),
      clearRect: vi.fn(),
      beginPath: vi.fn(),
      arc: vi.fn(),
      fill: vi.fn(),
      stroke: vi.fn(),
      moveTo: vi.fn(),
      lineTo: vi.fn(),
      createLinearGradient: vi.fn(() => ({ addColorStop: vi.fn() })),
      fillStyle: '',
      strokeStyle: '',
      globalAlpha: 1,
      lineWidth: 1,
      canvas: { width: 800, height: 600 },
    }
    HTMLCanvasElement.prototype.getContext = vi.fn(() => ctxMock)

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

    rafCallbacks = []
    rafId = 0
    originalRAF = global.requestAnimationFrame
    originalCAF = global.cancelAnimationFrame
    global.requestAnimationFrame = vi.fn((cb) => {
      rafId += 1
      rafCallbacks.push({ id: rafId, cb })
      return rafId
    })
    global.cancelAnimationFrame = vi.fn((id) => {
      rafCallbacks = rafCallbacks.filter((entry) => entry.id !== id)
    })

    originalInnerWidth = window.innerWidth
    originalInnerHeight = window.innerHeight
    Object.defineProperty(window, 'innerWidth', { value: 1024, configurable: true, writable: true })
    Object.defineProperty(window, 'innerHeight', { value: 768, configurable: true, writable: true })
  })

  afterEach(() => {
    cleanup()
    global.requestAnimationFrame = originalRAF
    global.cancelAnimationFrame = originalCAF
    Object.defineProperty(window, 'innerWidth', { value: originalInnerWidth, configurable: true, writable: true })
    Object.defineProperty(window, 'innerHeight', { value: originalInnerHeight, configurable: true, writable: true })
    vi.restoreAllMocks()
  })

  const flushFrame = () => {
    const pending = rafCallbacks.slice()
    rafCallbacks = []
    pending.forEach(({ cb }) => cb(performance.now()))
  }

  describe('rendering', () => {
    it('renders a canvas element', () => {
      const { container } = render(<ParticleBackground />)
      const canvas = container.querySelector('canvas')
      expect(canvas).toBeInTheDocument()
    })

    it('marks the canvas as aria-hidden for accessibility', () => {
      const { container } = render(<ParticleBackground />)
      const canvas = container.querySelector('canvas')
      expect(canvas).toHaveAttribute('aria-hidden', 'true')
    })

    it('applies fixed positioning classes', () => {
      const { container } = render(<ParticleBackground />)
      const canvas = container.querySelector('canvas')
      expect(canvas.className).toContain('absolute')
      expect(canvas.className).toContain('inset-0')
      expect(canvas.className).toContain('pointer-events-none')
    })

    it('applies inline z-index style', () => {
      const { container } = render(<ParticleBackground />)
      const canvas = container.querySelector('canvas')
      expect(canvas.style.zIndex).toBe('1')
    })
  })

  describe('canvas initialization', () => {
    it('requests a 2d context on the canvas', () => {
      render(<ParticleBackground />)
      expect(HTMLCanvasElement.prototype.getContext).toHaveBeenCalledWith('2d')
    })

    it('sizes the canvas to match the window dimensions', () => {
      const { container } = render(<ParticleBackground />)
      const canvas = container.querySelector('canvas')
      expect(canvas.width).toBe(1024)
      expect(canvas.height).toBe(768)
    })

    it('resizes the canvas when the window resize event fires', () => {
      const { container } = render(<ParticleBackground />)
      const canvas = container.querySelector('canvas')

      Object.defineProperty(window, 'innerWidth', { value: 1600, configurable: true, writable: true })
      Object.defineProperty(window, 'innerHeight', { value: 900, configurable: true, writable: true })
      window.dispatchEvent(new Event('resize'))

      expect(canvas.width).toBe(1600)
      expect(canvas.height).toBe(900)
    })
  })

  describe('IntersectionObserver integration', () => {
    it('creates an IntersectionObserver with the expected options', () => {
      render(<ParticleBackground />)
      expect(global.IntersectionObserver).toHaveBeenCalledTimes(1)
      const [, options] = global.IntersectionObserver.mock.calls[0]
      expect(options).toEqual({ threshold: 0, rootMargin: '100px' })
    })

    it('observes the canvas element', () => {
      const { container } = render(<ParticleBackground />)
      const canvas = container.querySelector('canvas')
      expect(observerInstances).toHaveLength(1)
      expect(observerInstances[0].observe).toHaveBeenCalledWith(canvas)
    })

    it('skips drawing when the canvas is offscreen', () => {
      render(<ParticleBackground />)
      flushFrame()
      ctxMock.clearRect.mockClear()

      observerInstances[0].callback([{ isIntersecting: false }])
      flushFrame()

      expect(ctxMock.clearRect).not.toHaveBeenCalled()
    })

    it('resumes drawing after becoming visible again', () => {
      render(<ParticleBackground />)
      flushFrame()

      observerInstances[0].callback([{ isIntersecting: false }])
      flushFrame()
      ctxMock.clearRect.mockClear()

      observerInstances[0].callback([{ isIntersecting: true }])
      flushFrame()

      expect(ctxMock.clearRect).toHaveBeenCalled()
    })
  })

  describe('animation loop', () => {
    it('schedules an animation frame on mount', () => {
      render(<ParticleBackground />)
      expect(global.requestAnimationFrame).toHaveBeenCalled()
    })

    it('clears the canvas and draws particles on each animated frame', () => {
      render(<ParticleBackground />)
      ctxMock.clearRect.mockClear()
      ctxMock.arc.mockClear()
      ctxMock.fill.mockClear()

      flushFrame()

      expect(ctxMock.clearRect).toHaveBeenCalledWith(0, 0, 1024, 768)
      expect(ctxMock.arc).toHaveBeenCalled()
      expect(ctxMock.fill).toHaveBeenCalled()
    })

    it('reschedules the next frame after drawing', () => {
      render(<ParticleBackground />)
      const initialCalls = global.requestAnimationFrame.mock.calls.length
      flushFrame()
      expect(global.requestAnimationFrame.mock.calls.length).toBeGreaterThan(initialCalls)
    })
  })

  describe('cleanup on unmount', () => {
    it('disconnects the IntersectionObserver', () => {
      const { unmount } = render(<ParticleBackground />)
      unmount()
      expect(observerInstances[0].disconnect).toHaveBeenCalled()
    })

    it('removes the window resize listener', () => {
      const removeSpy = vi.spyOn(window, 'removeEventListener')
      const { unmount } = render(<ParticleBackground />)
      unmount()
      const resizeRemoved = removeSpy.mock.calls.some(([event]) => event === 'resize')
      expect(resizeRemoved).toBe(true)
    })

    it('cancels the pending animation frame', () => {
      const { unmount } = render(<ParticleBackground />)
      unmount()
      expect(global.cancelAnimationFrame).toHaveBeenCalled()
    })
  })

  describe('edge cases', () => {
    it('handles very small viewport sizes without crashing', () => {
      Object.defineProperty(window, 'innerWidth', { value: 10, configurable: true, writable: true })
      Object.defineProperty(window, 'innerHeight', { value: 10, configurable: true, writable: true })

      expect(() => {
        const { unmount } = render(<ParticleBackground />)
        flushFrame()
        unmount()
      }).not.toThrow()
    })

    it('caps particle count so arc is not called excessively on large viewports', () => {
      Object.defineProperty(window, 'innerWidth', { value: 5000, configurable: true, writable: true })
      Object.defineProperty(window, 'innerHeight', { value: 5000, configurable: true, writable: true })

      render(<ParticleBackground />)
      ctxMock.arc.mockClear()
      flushFrame()

      expect(ctxMock.arc.mock.calls.length).toBeLessThanOrEqual(100)
    })

    it('does not throw when resize fires after unmount', () => {
      const { unmount } = render(<ParticleBackground />)
      unmount()
      expect(() => window.dispatchEvent(new Event('resize'))).not.toThrow()
    })

    it('supports mounting multiple instances independently', () => {
      const first = render(<ParticleBackground />)
      const second = render(<ParticleBackground />)

      expect(observerInstances).toHaveLength(2)
      expect(first.container.querySelector('canvas')).toBeInTheDocument()
      expect(second.container.querySelector('canvas')).toBeInTheDocument()

      first.unmount()
      second.unmount()
    })
  })
})
