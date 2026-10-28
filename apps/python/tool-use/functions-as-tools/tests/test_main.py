from src.main import main


def test_main(capsys):
    # Execute our application entry point
    main()

    # Capture Standard output from print()
    captured = capsys.readouterr()

    # Verify the expected message
    assert captured.out.strip() == ("Hello World! Agentic AI Module 3: Tool Use")
