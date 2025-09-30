#!/usr/bin/env python3
"""
Demonstration of the standalone Battleships engine
Shows how the same engine can power multiple platforms
"""

from battleships.engine import BattleshipEngine
from battleships.models import GameResult


def demo_pure_engine():
    """Demonstrate the engine without any I/O dependencies"""
    print("🎯 STANDALONE ENGINE DEMONSTRATION")
    print("=" * 50)
    
    # Create engine - note: no I/O dependencies!
    engine = BattleshipEngine(max_attempts=3, battleship_count=2)
    
    print("\n1. Initialize game:")
    state = engine.initialize_game()
    print(f"   ✓ Game initialized: {state['game_initialized']}")
    print(f"   ✓ Battleships to find: {state['total_battleships']}")
    print(f"   ✓ Attempts available: {state['attempts_remaining']}")
    
    print("\n2. Show board (debug mode):")
    board = engine.get_board_display(show_battleships=True)
    print(board)
    
    print("\n3. Make some guesses:")
    positions_to_try = [1, 3, 5, 7, 9]
    
    for pos in positions_to_try:
        if engine.is_game_over():
            break
            
        result = engine.make_guess(pos)
        
        if 'error' in result:
            print(f"   ❌ Position {pos}: {result['error']}")
        else:
            print(f"   🎯 Position {pos}: {result['message']}")
            print(f"      Attempts left: {result['attempts_remaining']}")
            print(f"      Battleships sunk: {result['battleships_sunk']}")
    
    print("\n4. Final result:")
    final_result = engine.get_game_result()
    print(f"   Game result: {final_result.value}")
    
    print("\n5. Final board (all revealed):")
    final_board = engine.get_board_display(show_battleships=True)
    print(final_board)
    
    print("\n✨ ENGINE DEMO COMPLETE - No I/O dependencies used!")


def demo_multiple_engines():
    """Demonstrate multiple concurrent engine instances"""
    print("\n\n🔄 MULTIPLE ENGINES DEMONSTRATION")
    print("=" * 50)
    
    # Create multiple engines
    engines = {
        'Easy': BattleshipEngine(max_attempts=10, battleship_count=2),
        'Normal': BattleshipEngine(max_attempts=5, battleship_count=3),
        'Hard': BattleshipEngine(max_attempts=3, battleship_count=4)
    }
    
    print("\nInitializing multiple game modes...")
    for name, engine in engines.items():
        state = engine.initialize_game()
        print(f"   ✓ {name} mode: {state['total_battleships']} ships, "
              f"{state['attempts_remaining']} attempts")
    
    print("\nTesting same guess across all modes:")
    test_position = 5
    
    for name, engine in engines.items():
        result = engine.make_guess(test_position)
        print(f"   {name}: Position {test_position} → {result['message']}")
    
    print("\n✨ MULTIPLE ENGINES DEMO COMPLETE")


def demo_stateful_behavior():
    """Demonstrate engine's stateful behavior"""
    print("\n\n💾 STATEFUL BEHAVIOR DEMONSTRATION")
    print("=" * 50)
    
    engine = BattleshipEngine()
    
    print("\n1. Before initialization:")
    try:
        result = engine.make_guess(5)
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Expected error: {e}")
    
    print("\n2. After initialization:")
    engine.initialize_game()
    result = engine.make_guess(5)
    print(f"   First guess at 5: {result['message']}")
    
    print("\n3. Repeated guess:")
    result = engine.make_guess(5)
    print(f"   Second guess at 5: {result['message']}")
    
    print("\n4. Engine remembers state between calls!")
    state = engine.get_game_state()
    print(f"   Attempts used: {state['attempts_used']}")
    print(f"   Game still active: {not engine.is_game_over()}")
    
    print("\n✨ STATEFUL DEMO COMPLETE")


def demo_json_serializable():
    """Demonstrate that engine responses are JSON-serializable"""
    print("\n\n📄 JSON SERIALIZATION DEMONSTRATION")
    print("=" * 50)
    
    import json
    
    engine = BattleshipEngine()
    state = engine.initialize_game()
    
    print("\n1. Engine state is JSON-serializable:")
    json_state = json.dumps(state, indent=2)
    print(json_state[:200] + "..." if len(json_state) > 200 else json_state)
    
    print("\n2. Guess results are JSON-serializable:")
    result = engine.make_guess(1)
    json_result = json.dumps(result, indent=2)
    print(json_result[:200] + "..." if len(json_result) > 200 else json_result)
    
    print("\n✨ Perfect for REST APIs, message queues, etc!")


def main():
    """Run all demonstrations"""
    print("🚢 BATTLESHIPS STANDALONE ENGINE SHOWCASE")
    print("This demonstrates a truly platform-agnostic game engine")
    print("The same engine powers console, web, mobile, desktop, etc.\n")
    
    demo_pure_engine()
    demo_multiple_engines() 
    demo_stateful_behavior()
    demo_json_serializable()
    
    print("\n\n🎉 ALL DEMONSTRATIONS COMPLETE!")
    print("\nKey Benefits Demonstrated:")
    print("• ✅ No I/O dependencies - pure logic")
    print("• ✅ Concurrent instances - multi-tenancy ready")  
    print("• ✅ Stateful behavior - maintains game state")
    print("• ✅ JSON serializable - perfect for APIs")
    print("• ✅ Error handling - graceful failure modes")
    print("\nThis engine can power ANY platform! 🚀")


if __name__ == "__main__":
    main()