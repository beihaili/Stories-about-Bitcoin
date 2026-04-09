import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ErrorBoundary from '../ErrorBoundary'

const ThrowingChild = ({ shouldThrow = true }) => {
  if (shouldThrow) throw new Error('test error')
  return <div>child content</div>
}

describe('ErrorBoundary', () => {
  beforeEach(() => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders children when no error occurs', () => {
    render(
      <ErrorBoundary>
        <div>hello world</div>
      </ErrorBoundary>
    )
    expect(screen.getByText('hello world')).toBeInTheDocument()
  })

  it('renders multiple children without error', () => {
    render(
      <ErrorBoundary>
        <span>first</span>
        <span>second</span>
      </ErrorBoundary>
    )
    expect(screen.getByText('first')).toBeInTheDocument()
    expect(screen.getByText('second')).toBeInTheDocument()
  })

  it('shows Chinese error UI by default when child throws', () => {
    render(
      <ErrorBoundary>
        <ThrowingChild />
      </ErrorBoundary>
    )
    expect(screen.getByText('加载出错了')).toBeInTheDocument()
    expect(screen.getByText('这个部分暂时无法显示，请刷新页面重试。')).toBeInTheDocument()
    expect(screen.getByText('刷新页面')).toBeInTheDocument()
  })

  it('shows Chinese error UI when lang="zh"', () => {
    render(
      <ErrorBoundary lang="zh">
        <ThrowingChild />
      </ErrorBoundary>
    )
    expect(screen.getByText('加载出错了')).toBeInTheDocument()
    expect(screen.getByText('刷新页面')).toBeInTheDocument()
  })

  it('shows English error UI when lang="en"', () => {
    render(
      <ErrorBoundary lang="en">
        <ThrowingChild />
      </ErrorBoundary>
    )
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
    expect(screen.getByText('This section could not be loaded. Please refresh the page to try again.')).toBeInTheDocument()
    expect(screen.getByText('Refresh page')).toBeInTheDocument()
  })

  it('does not show error UI when children render successfully', () => {
    render(
      <ErrorBoundary>
        <ThrowingChild shouldThrow={false} />
      </ErrorBoundary>
    )
    expect(screen.getByText('child content')).toBeInTheDocument()
    expect(screen.queryByText('加载出错了')).not.toBeInTheDocument()
  })

  it('calls window.location.reload when retry button is clicked', async () => {
    const user = userEvent.setup()
    const reloadMock = vi.fn()
    Object.defineProperty(window, 'location', {
      value: { reload: reloadMock },
      writable: true,
      configurable: true,
    })

    render(
      <ErrorBoundary>
        <ThrowingChild />
      </ErrorBoundary>
    )

    await user.click(screen.getByText('刷新页面'))
    expect(reloadMock).toHaveBeenCalledOnce()
  })

  it('catches errors only in its own subtree', () => {
    render(
      <div>
        <div data-testid="outside">safe content</div>
        <ErrorBoundary>
          <ThrowingChild />
        </ErrorBoundary>
      </div>
    )
    expect(screen.getByTestId('outside')).toHaveTextContent('safe content')
    expect(screen.getByText('加载出错了')).toBeInTheDocument()
  })
})
