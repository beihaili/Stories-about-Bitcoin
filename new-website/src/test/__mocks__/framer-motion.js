import React from 'react'

function createMotionProxy() {
  return new Proxy({}, {
    get(_target, prop) {
      return React.forwardRef(function MotionComponent({ children, ...props }, ref) {
        // Strip framer-motion specific props
        const domProps = {}
        for (const [key, value] of Object.entries(props)) {
          if (
            !key.startsWith('while') &&
            !key.startsWith('animate') &&
            !key.startsWith('initial') &&
            !key.startsWith('exit') &&
            !key.startsWith('transition') &&
            !key.startsWith('variants') &&
            key !== 'layout' &&
            key !== 'layoutId' &&
            key !== 'viewport'
          ) {
            domProps[key] = value
          }
        }
        return React.createElement(prop, { ...domProps, ref }, children)
      })
    },
  })
}

export const motion = createMotionProxy()

export function AnimatePresence({ children }) {
  return React.createElement(React.Fragment, null, children)
}

export function useAnimation() {
  return { start: () => {}, stop: () => {} }
}

export function useInView() {
  return [null, true]
}
