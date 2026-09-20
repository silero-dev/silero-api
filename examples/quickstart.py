        """Minimal Silero example: create one prediction and print the output URL(s)."""
        import silero_api

        output = silero_api.run({
    "text": "Hello, this is a test of MiMo speech synthesis."
})
        print(output)
