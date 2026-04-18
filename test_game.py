import unittest
from unittest.mock import patch, MagicMock
from game import determine_winner, play_game, CHOICES


class TestDetermineWinner(unittest.TestCase):
    """Test cases for the determine_winner function"""
    
    # Test tie scenarios
    def test_tie_rock_vs_rock(self):
        """Test that rock vs rock is a tie"""
        self.assertEqual(determine_winner('rock', 'rock'), 'tie')
    
    def test_tie_paper_vs_paper(self):
        """Test that paper vs paper is a tie"""
        self.assertEqual(determine_winner('paper', 'paper'), 'tie')
    
    def test_tie_scissors_vs_scissors(self):
        """Test that scissors vs scissors is a tie"""
        self.assertEqual(determine_winner('scissors', 'scissors'), 'tie')
    
    # Test user win scenarios
    def test_user_wins_rock_vs_scissors(self):
        """Test that rock beats scissors"""
        self.assertEqual(determine_winner('rock', 'scissors'), 'user')
    
    def test_user_wins_paper_vs_rock(self):
        """Test that paper beats rock"""
        self.assertEqual(determine_winner('paper', 'rock'), 'user')
    
    def test_user_wins_scissors_vs_paper(self):
        """Test that scissors beats paper"""
        self.assertEqual(determine_winner('scissors', 'paper'), 'user')
    
    # Test computer win scenarios
    def test_computer_wins_scissors_vs_rock(self):
        """Test that scissors loses to rock"""
        self.assertEqual(determine_winner('scissors', 'rock'), 'computer')
    
    def test_computer_wins_rock_vs_paper(self):
        """Test that rock loses to paper"""
        self.assertEqual(determine_winner('rock', 'paper'), 'computer')
    
    def test_computer_wins_paper_vs_scissors(self):
        """Test that paper loses to scissors"""
        self.assertEqual(determine_winner('paper', 'scissors'), 'computer')
    
    # Test invalid input
    def test_invalid_choice_returns_none(self):
        """Test that invalid user choice returns None"""
        self.assertIsNone(determine_winner('invalid', 'rock'))
    
    def test_empty_string_returns_none(self):
        """Test that empty string returns None"""
        self.assertIsNone(determine_winner('', 'rock'))
    
    def test_uppercase_invalid_returns_none(self):
        """Test that uppercase invalid choice returns None"""
        self.assertIsNone(determine_winner('ROCK', 'rock'))
    
    # Test that valid choices are defined
    def test_choices_contains_rock(self):
        """Test that CHOICES contains 'rock'"""
        self.assertIn('rock', CHOICES)
    
    def test_choices_contains_paper(self):
        """Test that CHOICES contains 'paper'"""
        self.assertIn('paper', CHOICES)
    
    def test_choices_contains_scissors(self):
        """Test that CHOICES contains 'scissors'"""
        self.assertIn('scissors', CHOICES)
    
    def test_choices_has_three_items(self):
        """Test that CHOICES has exactly 3 items"""
        self.assertEqual(len(CHOICES), 3)


class TestInputValidation(unittest.TestCase):
    """Test cases for input validation and edge cases"""
    
    def test_whitespace_with_leading_space(self):
        """Test that leading whitespace is invalid"""
        self.assertIsNone(determine_winner(' rock', 'paper'))
    
    def test_whitespace_with_trailing_space(self):
        """Test that trailing whitespace is invalid"""
        self.assertIsNone(determine_winner('rock ', 'paper'))
    
    def test_whitespace_with_both_spaces(self):
        """Test that spaces on both sides are invalid"""
        self.assertIsNone(determine_winner(' rock ', 'paper'))
    
    def test_mixed_case_uppercase_rock(self):
        """Test that uppercase ROCK is invalid"""
        self.assertIsNone(determine_winner('ROCK', 'scissors'))
    
    def test_mixed_case_capitalized_paper(self):
        """Test that capitalized Paper is invalid"""
        self.assertIsNone(determine_winner('Paper', 'rock'))
    
    def test_mixed_case_mixed_scissors(self):
        """Test that mixed case ScIssoRs is invalid"""
        self.assertIsNone(determine_winner('ScIssoRs', 'paper'))
    
    def test_numeric_string_input(self):
        """Test that numeric strings are invalid"""
        self.assertIsNone(determine_winner('1', 'rock'))
    
    def test_special_characters(self):
        """Test that special characters are invalid"""
        self.assertIsNone(determine_winner('rock!', 'paper'))
    
    def test_none_as_user_choice(self):
        """Test that None as user choice returns None"""
        self.assertIsNone(determine_winner(None, 'rock'))
    
    def test_very_long_string(self):
        """Test that very long strings are invalid"""
        self.assertIsNone(determine_winner('rock' * 100, 'scissors'))


class TestPlayGameIntegration(unittest.TestCase):
    """Integration tests for the play_game function"""
    
    @patch('game.random.choice')
    @patch('builtins.input', side_effect=['rock', 'no'])
    @patch('builtins.print')
    def test_play_game_user_tie(self, mock_print, mock_input, mock_random):
        """Test that a tie is correctly displayed"""
        mock_random.return_value = 'rock'
        play_game()
        
        # Check that tie message was printed
        printed_messages = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("It's a tie!", printed_messages)
    
    @patch('game.random.choice')
    @patch('builtins.input', side_effect=['rock', 'no'])
    @patch('builtins.print')
    def test_play_game_user_wins(self, mock_print, mock_input, mock_random):
        """Test that a user win is correctly displayed"""
        mock_random.return_value = 'scissors'
        play_game()
        
        printed_messages = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("You win!", printed_messages)
    
    @patch('game.random.choice')
    @patch('builtins.input', side_effect=['rock', 'no'])
    @patch('builtins.print')
    def test_play_game_computer_wins(self, mock_print, mock_input, mock_random):
        """Test that a computer win is correctly displayed"""
        mock_random.return_value = 'paper'
        play_game()
        
        printed_messages = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("Computer wins!", printed_messages)
    
    @patch('builtins.input', side_effect=['invalid', 'no'])
    @patch('builtins.print')
    def test_play_game_invalid_choice(self, mock_print, mock_input):
        """Test that invalid choice is handled correctly"""
        play_game()
        
        printed_messages = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("Invalid choice. Please try again.", printed_messages)
    
    @patch('game.random.choice')
    @patch('builtins.input', side_effect=['rock', 'no'])
    @patch('builtins.print')
    def test_play_game_computer_choice_displayed(self, mock_print, mock_input, mock_random):
        """Test that computer's choice is displayed"""
        mock_random.return_value = 'scissors'
        play_game()
        
        printed_messages = [call[0][0] for call in mock_print.call_args_list]
        self.assertTrue(any("Computer chose:" in str(msg) for msg in printed_messages))
    
    @patch('game.random.choice')
    @patch('builtins.input', side_effect=['rock', 'yes', 'paper', 'no'])
    @patch('builtins.print')
    def test_play_game_play_again_yes(self, mock_print, mock_input, mock_random):
        """Test that game can be played again when user chooses yes"""
        mock_random.return_value = 'scissors'
        play_game()
        
        # Should have called input twice (first game and play again prompt)
        # Then called again for second game
        self.assertGreaterEqual(mock_input.call_count, 3)
    
    @patch('game.random.choice')
    @patch('builtins.input', side_effect=['rock', 'no'])
    @patch('builtins.print')
    def test_play_game_goodbye_message(self, mock_print, mock_input, mock_random):
        """Test that goodbye message is displayed when user chooses no"""
        mock_random.return_value = 'scissors'
        play_game()
        
        printed_messages = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("Thanks for playing! Goodbye!", printed_messages)


class TestComputerChoice(unittest.TestCase):
    """Test cases for computer choice validation"""
    
    @patch('game.random.choice')
    @patch('builtins.input', side_effect=['rock', 'no'])
    @patch('builtins.print')
    def test_computer_choice_is_valid(self, mock_print, mock_input, mock_random):
        """Test that computer choice is always from valid options"""
        for choice in CHOICES:
            mock_random.return_value = choice
            mock_input.side_effect = ['rock', 'no']
            mock_print.reset_mock()
            play_game()
            self.assertIn(choice, CHOICES)


if __name__ == '__main__':
    unittest.main()
