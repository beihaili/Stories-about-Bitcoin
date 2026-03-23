import { render, screen, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import BackToTop from '../BackToTop'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

describe('BackToTop', () => {
  let scrollHandler

  beforeEach(() => {
    scrollHandler = null
    vi.spyOn(window, 'addEventListener').mockImplementation((event, handler) => {
      if (event === 'scroll') scrollHandler = handler
    })
    vi.spyOn(window, 'removeEventListener').mockImplementation(() => {})
    vi.spyOn(window, 'scrollTo').mockImplementation(() => {})
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('is hidden when scrollY < 400', () => {
    render(<BackToTop lang="zh" />)
    expect(screen.queryByLabelText('返回顶部')).not.toBeInTheDocument()
  })

  it('appears when scrollY >= 400', () => {
    render(<BackToTop lang="zh" />)
    Object.defineProperty(window, 'scrollY', { value: 500, writable: true })
    act(() => scrollHandler())
    expect(screen.getByLabelText('返回顶部')).toBeInTheDocument()
  })

  it('calls scrollTo on click', async () => {
    const user = userEvent.setup()
    render(<BackToTop lang="zh" />)
    Object.defineProperty(window, 'scrollY', { value: 500, writable: true })
    act(() => scrollHandler())
    await user.click(screen.getByLabelText('返回顶部'))
    expect(window.scrollTo).toHaveBeenCalledWith({ top: 0, behavior: 'smooth' })
  })

  it('renders Chinese aria-label', () => {
    render(<BackToTop lang="zh" />)
    Object.defineProperty(window, 'scrollY', { value: 500, writable: true })
    act(() => scrollHandler())
    expect(screen.getByLabelText('返回顶部')).toBeInTheDocument()
  })

  it('renders English aria-label', () => {
    render(<BackToTop lang="en" />)
    Object.defineProperty(window, 'scrollY', { value: 500, writable: true })
    act(() => scrollHandler())
    expect(screen.getByLabelText('Back to top')).toBeInTheDocument()
  })
})
