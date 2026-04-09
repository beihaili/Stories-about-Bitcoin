import { render, screen } from '@testing-library/react'
import { cleanup } from '@testing-library/react'
import GiscusComments from '../GiscusComments'

describe('GiscusComments', () => {
  afterEach(() => {
    cleanup()
  })

  it('renders Chinese title and subtitle by default', () => {
    render(<GiscusComments />)
    expect(screen.getByText('读者讨论区')).toBeInTheDocument()
    expect(screen.getByText('基于 GitHub Discussions，登录 GitHub 即可参与讨论')).toBeInTheDocument()
  })

  it('renders English title and subtitle when lang is en', () => {
    render(<GiscusComments lang="en" />)
    expect(screen.getByText('Reader Discussions')).toBeInTheDocument()
    expect(screen.getByText('Powered by GitHub Discussions. Sign in with GitHub to comment.')).toBeInTheDocument()
  })

  it('renders section with correct layout classes', () => {
    render(<GiscusComments />)
    const section = screen.getByText('读者讨论区').closest('section')
    expect(section).toHaveClass('bg-historical-parchment', 'dark:bg-gray-900')
  })

  it('renders the giscus container div', () => {
    const { container } = render(<GiscusComments />)
    expect(container.querySelector('.giscus-container')).toBeInTheDocument()
  })

  it('appends a giscus script to the container', () => {
    const { container } = render(<GiscusComments />)
    const script = container.querySelector('.giscus-container script')
    expect(script).not.toBeNull()
    expect(script.src).toBe('https://giscus.app/client.js')
  })

  it('sets correct repo configuration on the script', () => {
    const { container } = render(<GiscusComments />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('data-repo')).toBe('beihaili/Stories-about-Bitcoin')
    expect(script.getAttribute('data-repo-id')).toBe('R_kgDOPnWv-w')
    expect(script.getAttribute('data-category')).toBe('Announcements')
    expect(script.getAttribute('data-category-id')).toBe('DIC_kwDOPnWv-84C2Btd')
  })

  it('sets data-mapping to pathname with strict mode', () => {
    const { container } = render(<GiscusComments />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('data-mapping')).toBe('pathname')
    expect(script.getAttribute('data-strict')).toBe('1')
  })

  it('sets data-theme to light by default', () => {
    const { container } = render(<GiscusComments />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('data-theme')).toBe('light')
  })

  it('sets data-theme to dark when theme prop is dark', () => {
    const { container } = render(<GiscusComments theme="dark" />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('data-theme')).toBe('dark')
  })

  it('sets data-theme to light for non-dark theme values', () => {
    const { container } = render(<GiscusComments theme="custom" />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('data-theme')).toBe('light')
  })

  it('sets data-lang to zh-CN when lang is zh', () => {
    const { container } = render(<GiscusComments lang="zh" />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('data-lang')).toBe('zh-CN')
  })

  it('sets data-lang to en when lang is en', () => {
    const { container } = render(<GiscusComments lang="en" />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('data-lang')).toBe('en')
  })

  it('sets script as async with lazy loading', () => {
    const { container } = render(<GiscusComments />)
    const script = container.querySelector('.giscus-container script')
    expect(script.async).toBe(true)
    expect(script.getAttribute('data-loading')).toBe('lazy')
  })

  it('sets crossorigin to anonymous', () => {
    const { container } = render(<GiscusComments />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('crossorigin')).toBe('anonymous')
  })

  it('removes existing script when re-rendered with new props', () => {
    const { container, rerender } = render(<GiscusComments lang="zh" theme="light" />)
    const giscusContainer = container.querySelector('.giscus-container')
    expect(giscusContainer.querySelectorAll('script')).toHaveLength(1)

    rerender(<GiscusComments lang="en" theme="dark" />)
    expect(giscusContainer.querySelectorAll('script')).toHaveLength(1)
    const script = giscusContainer.querySelector('script')
    expect(script.getAttribute('data-lang')).toBe('en')
    expect(script.getAttribute('data-theme')).toBe('dark')
  })

  it('removes existing .giscus element when re-rendered', () => {
    const { container, rerender } = render(<GiscusComments />)
    const giscusContainer = container.querySelector('.giscus-container')

    const fakeIframe = document.createElement('div')
    fakeIframe.className = 'giscus'
    giscusContainer.appendChild(fakeIframe)
    expect(giscusContainer.querySelector('.giscus')).not.toBeNull()

    rerender(<GiscusComments lang="en" />)
    expect(giscusContainer.querySelector('.giscus')).toBeNull()
  })

  it('enables reactions and sets input position to top', () => {
    const { container } = render(<GiscusComments />)
    const script = container.querySelector('.giscus-container script')
    expect(script.getAttribute('data-reactions-enabled')).toBe('1')
    expect(script.getAttribute('data-input-position')).toBe('top')
    expect(script.getAttribute('data-emit-metadata')).toBe('0')
  })
})
