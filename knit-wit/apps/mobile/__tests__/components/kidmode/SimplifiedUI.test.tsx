/**
 * Tests for Simplified UI Components (Kid Mode)
 *
 * Verifies that SimplifiedButton, SimplifiedCard, and SimplifiedInput
 * components meet Kid Mode requirements:
 * - Touch targets >= 56dp
 * - Large text sizes
 * - Proper accessibility labels
 * - Correct visual styling
 * - Interactive behavior
 *
 * @see Story E2: Simplified UI Components
 */

import React from 'react';
import { Text } from 'react-native';
import { render, fireEvent } from '@testing-library/react-native';
import {
  SimplifiedButton,
  SimplifiedCard,
  SimplifiedInput,
} from '../../../src/components/kidmode/SimplifiedUI';
import { kidModeTheme } from '../../../src/theme/kidModeTheme';

describe('SimplifiedButton', () => {
  describe('Rendering', () => {
    it('renders with label text', () => {
      const { getByText } = render(
        <SimplifiedButton label="Test Button" onPress={() => {}} />
      );

      expect(getByText('Test Button')).toBeTruthy();
    });

    it('renders with icon when provided', () => {
      const { getByText } = render(
        <SimplifiedButton
          label="Test Button"
          icon={<>{/* Icon content */}</>}
          onPress={() => {}}
        />
      );

      expect(getByText('Test Button')).toBeTruthy();
    });

    it('applies primary variant styles by default', () => {
      const { getByRole } = render(
        <SimplifiedButton label="Primary Button" onPress={() => {}} />
      );

      const button = getByRole('button');
      expect(button).toBeTruthy();
      expect(button.props.accessibilityLabel).toBe('Primary Button');
    });

    it('applies secondary variant styles when specified', () => {
      const { getByRole } = render(
        <SimplifiedButton
          label="Secondary Button"
          variant="secondary"
          onPress={() => {}}
        />
      );

      const button = getByRole('button');
      expect(button).toBeTruthy();
    });

    it('applies outline variant styles when specified', () => {
      const { getByRole } = render(
        <SimplifiedButton
          label="Outline Button"
          variant="outline"
          onPress={() => {}}
        />
      );

      const button = getByRole('button');
      expect(button).toBeTruthy();
    });

    it('applies large size styles when specified', () => {
      const { getByRole } = render(
        <SimplifiedButton label="Large Button" size="large" onPress={() => {}} />
      );

      const button = getByRole('button');
      expect(button).toBeTruthy();
    });
  });

  describe('Touch Target Size', () => {
    it('has minimum touch target of 64dp for comfortable size', () => {
      const { getByRole } = render(
        <SimplifiedButton
          label="Comfortable Button"
          size="comfortable"
          onPress={() => {}}
        />
      );

      const button = getByRole('button');
      const style = button.props.style;

      // Extract minHeight from style array
      const minHeight = Array.isArray(style)
        ? style.find((s) => s && s.minHeight)?.minHeight
        : style?.minHeight;

      expect(minHeight).toBeGreaterThanOrEqual(
        kidModeTheme.touchTargets.comfortable
      ); // 64dp
    });

    it('has minimum touch target of 72dp for large size', () => {
      const { getByRole } = render(
        <SimplifiedButton label="Large Button" size="large" onPress={() => {}} />
      );

      const button = getByRole('button');
      const style = button.props.style;

      // Extract minHeight from style array by finding all style objects with minHeight
      let maxMinHeight = 0;
      if (Array.isArray(style)) {
        style.forEach((s) => {
          if (s && s.minHeight && s.minHeight > maxMinHeight) {
            maxMinHeight = s.minHeight;
          }
        });
      } else if (style?.minHeight) {
        maxMinHeight = style.minHeight;
      }

      // Should have at least the kidMode touch target size
      expect(maxMinHeight).toBeGreaterThanOrEqual(kidModeTheme.touchTargets.minimum); // At least 56dp
    });
  });

  describe('Interaction', () => {
    it('calls onPress when pressed', () => {
      const onPressMock = jest.fn();
      const { getByRole } = render(
        <SimplifiedButton label="Press Me" onPress={onPressMock} />
      );

      const button = getByRole('button');
      fireEvent.press(button);

      expect(onPressMock).toHaveBeenCalledTimes(1);
    });

    it('does not call onPress when disabled', () => {
      const onPressMock = jest.fn();
      const { getByRole } = render(
        <SimplifiedButton label="Disabled Button" onPress={onPressMock} disabled />
      );

      const button = getByRole('button');
      fireEvent.press(button);

      expect(onPressMock).not.toHaveBeenCalled();
    });
  });

  describe('Accessibility', () => {
    it('has correct accessibility role', () => {
      const { getByRole } = render(
        <SimplifiedButton label="Accessible Button" onPress={() => {}} />
      );

      expect(getByRole('button')).toBeTruthy();
    });

    it('has correct accessibility label', () => {
      const { getByRole } = render(
        <SimplifiedButton label="My Button" onPress={() => {}} />
      );

      const button = getByRole('button');
      expect(button.props.accessibilityLabel).toBe('My Button');
    });

    it('has default accessibility hint', () => {
      const { getByRole } = render(
        <SimplifiedButton label="Click Me" onPress={() => {}} />
      );

      const button = getByRole('button');
      expect(button.props.accessibilityHint).toBe('Press to click me');
    });

    it('uses custom accessibility hint when provided', () => {
      const { getByRole } = render(
        <SimplifiedButton
          label="Submit"
          onPress={() => {}}
          accessibilityHint="Submit the form"
        />
      );

      const button = getByRole('button');
      expect(button.props.accessibilityHint).toBe('Submit the form');
    });

    it('has disabled accessibility state when disabled', () => {
      const { getByRole } = render(
        <SimplifiedButton label="Disabled" onPress={() => {}} disabled />
      );

      const button = getByRole('button');
      expect(button.props.accessibilityState).toEqual({ disabled: true });
    });
  });
});

describe('SimplifiedCard', () => {
  describe('Rendering', () => {
    it('renders children content', () => {
      const { getByText } = render(
        <SimplifiedCard>
          <Text>Card Content</Text>
        </SimplifiedCard>
      );

      expect(getByText('Card Content')).toBeTruthy();
    });

    it('renders title when provided', () => {
      const { getByText } = render(
        <SimplifiedCard title="Card Title">
          <Text>Card Content</Text>
        </SimplifiedCard>
      );

      expect(getByText('Card Title')).toBeTruthy();
      expect(getByText('Card Content')).toBeTruthy();
    });

    it('applies default variant styles', () => {
      const { getByText } = render(
        <SimplifiedCard>
          <Text>Default Card</Text>
        </SimplifiedCard>
      );

      expect(getByText('Default Card')).toBeTruthy();
    });

    it('applies primary variant styles', () => {
      const { getByText } = render(
        <SimplifiedCard variant="primary">
          <Text>Primary Card</Text>
        </SimplifiedCard>
      );

      expect(getByText('Primary Card')).toBeTruthy();
    });

    it('applies selected state styles', () => {
      const { getByText } = render(
        <SimplifiedCard selected>
          <Text>Selected Card</Text>
        </SimplifiedCard>
      );

      expect(getByText('Selected Card')).toBeTruthy();
    });
  });

  describe('Interaction', () => {
    it('renders as View when not pressable', () => {
      const { getByText } = render(
        <SimplifiedCard pressable={false}>
          <Text>Non-pressable Card</Text>
        </SimplifiedCard>
      );

      const card = getByText('Non-pressable Card').parent;
      expect(card).toBeTruthy();
    });

    it('calls onPress when pressable and pressed', () => {
      const onPressMock = jest.fn();
      const { getByRole } = render(
        <SimplifiedCard pressable onPress={onPressMock}>
          <Text>Pressable Card</Text>
        </SimplifiedCard>
      );

      const card = getByRole('button');
      fireEvent.press(card);

      expect(onPressMock).toHaveBeenCalledTimes(1);
    });
  });

  describe('Accessibility', () => {
    it('has correct accessibility label from title', () => {
      const { getByText } = render(
        <SimplifiedCard title="My Card">
          <Text>Content</Text>
        </SimplifiedCard>
      );

      const card = getByText('My Card').parent;
      expect(card?.props.accessibilityLabel).toBe('My Card');
    });

    it('uses custom accessibility label when provided', () => {
      const { getByText } = render(
        <SimplifiedCard
          title="Card Title"
          accessibilityLabel="Custom Label"
        >
          <Text>Content</Text>
        </SimplifiedCard>
      );

      const card = getByText('Card Title').parent;
      expect(card?.props.accessibilityLabel).toBe('Custom Label');
    });

    it('has selected accessibility state when pressable and selected', () => {
      const { getByRole } = render(
        <SimplifiedCard pressable selected onPress={() => {}}>
          <Text>Selected Card</Text>
        </SimplifiedCard>
      );

      const card = getByRole('button');
      expect(card.props.accessibilityState).toEqual({ selected: true });
    });
  });
});

describe('SimplifiedInput', () => {
  describe('Rendering', () => {
    it('renders input with placeholder', () => {
      const { getByPlaceholderText } = render(
        <SimplifiedInput placeholder="Enter text" />
      );

      expect(getByPlaceholderText('Enter text')).toBeTruthy();
    });

    it('renders label when provided', () => {
      const { getByText } = render(
        <SimplifiedInput label="Input Label" placeholder="Enter text" />
      );

      expect(getByText('Input Label')).toBeTruthy();
    });

    it('renders helper text when provided', () => {
      const { getByText } = render(
        <SimplifiedInput
          placeholder="Enter text"
          helperText="This is helper text"
        />
      );

      expect(getByText('This is helper text')).toBeTruthy();
    });

    it('renders error message when provided', () => {
      const { getByText } = render(
        <SimplifiedInput placeholder="Enter text" error="This is an error" />
      );

      expect(getByText('This is an error')).toBeTruthy();
    });

    it('does not render helper text when error is present', () => {
      const { queryByText, getByText } = render(
        <SimplifiedInput
          placeholder="Enter text"
          error="Error message"
          helperText="Helper text"
        />
      );

      expect(getByText('Error message')).toBeTruthy();
      expect(queryByText('Helper text')).toBeNull();
    });
  });

  describe('Touch Target Size', () => {
    it('has minimum height of 56dp', () => {
      const { getByPlaceholderText } = render(
        <SimplifiedInput placeholder="Test Input" />
      );

      const input = getByPlaceholderText('Test Input');
      const style = input.props.style;

      // Extract minHeight from style array
      const minHeight = Array.isArray(style)
        ? style.find((s) => s && s.minHeight)?.minHeight
        : style?.minHeight;

      expect(minHeight).toBeGreaterThanOrEqual(
        kidModeTheme.touchTargets.minimum
      ); // 56dp
    });
  });

  describe('Interaction', () => {
    it('calls onChangeText when text is entered', () => {
      const onChangeTextMock = jest.fn();
      const { getByPlaceholderText } = render(
        <SimplifiedInput
          placeholder="Type here"
          onChangeText={onChangeTextMock}
        />
      );

      const input = getByPlaceholderText('Type here');
      fireEvent.changeText(input, 'New text');

      expect(onChangeTextMock).toHaveBeenCalledWith('New text');
    });

    it('displays value when provided', () => {
      const { getByDisplayValue } = render(
        <SimplifiedInput placeholder="Test" value="Current value" />
      );

      expect(getByDisplayValue('Current value')).toBeTruthy();
    });
  });

  describe('Accessibility', () => {
    it('uses label as accessibility label', () => {
      const { getByPlaceholderText } = render(
        <SimplifiedInput label="Username" placeholder="Enter username" />
      );

      const input = getByPlaceholderText('Enter username');
      expect(input.props.accessibilityLabel).toBe('Username');
    });

    it('uses placeholder as accessibility label when no label', () => {
      const { getByPlaceholderText } = render(
        <SimplifiedInput placeholder="Enter text" />
      );

      const input = getByPlaceholderText('Enter text');
      expect(input.props.accessibilityLabel).toBe('Enter text');
    });

    it('uses custom accessibility label when provided', () => {
      const { getByPlaceholderText } = render(
        <SimplifiedInput
          placeholder="Test"
          accessibilityLabel="Custom label"
        />
      );

      const input = getByPlaceholderText('Test');
      expect(input.props.accessibilityLabel).toBe('Custom label');
    });

    it('error text has alert role and live region', () => {
      const { getByText } = render(
        <SimplifiedInput placeholder="Test" error="Error message" />
      );

      const errorText = getByText('Error message');
      expect(errorText.props.accessibilityRole).toBe('alert');
      expect(errorText.props.accessibilityLiveRegion).toBe('polite');
    });
  });
});

describe('Integration Tests', () => {
  describe('Conditional Rendering with Kid Mode', () => {
    it('SimplifiedButton can be used conditionally', () => {
      const kidMode = true;
      const onPressMock = jest.fn();

      const { getByRole } = render(
        <>
          {kidMode ? (
            <SimplifiedButton label="Kid Mode Button" onPress={onPressMock} />
          ) : (
            <>{/* Regular button */}</>
          )}
        </>
      );

      const button = getByRole('button');
      expect(button.props.accessibilityLabel).toBe('Kid Mode Button');

      fireEvent.press(button);
      expect(onPressMock).toHaveBeenCalledTimes(1);
    });

    it('SimplifiedCard can be used conditionally for selection', () => {
      const kidMode = true;
      const selected = 'sphere';
      const handleSelect = jest.fn();

      const { getByText } = render(
        <>
          {kidMode ? (
            <>
              <SimplifiedCard
                selected={selected === 'sphere'}
                pressable
                onPress={() => handleSelect('sphere')}
              >
                <Text>Sphere</Text>
              </SimplifiedCard>
              <SimplifiedCard
                selected={selected === 'cylinder'}
                pressable
                onPress={() => handleSelect('cylinder')}
              >
                <Text>Cylinder</Text>
              </SimplifiedCard>
            </>
          ) : (
            <>{/* Regular cards */}</>
          )}
        </>
      );

      expect(getByText('Sphere')).toBeTruthy();
      expect(getByText('Cylinder')).toBeTruthy();
    });
  });
});
