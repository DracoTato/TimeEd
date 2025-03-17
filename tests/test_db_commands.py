from app.db.commands import init_db, reset_db, init_superadmin, create_seed


def test_init_db(runner, app):
    with app.app_context():
        result = runner.invoke(init_db, input="n")

    assert result.exit_code == 0
    assert "successfully" in result.output


def test_reset_db_confirm_yes(runner, app):
    with app.app_context():
        result = runner.invoke(reset_db, input="y")

    assert result.exit_code == 0
    assert "[y/N]" in result.output
    assert "successfully" in result.output


def test_reset_db_confirm_no(runner, app):
    with app.app_context():
        result = runner.invoke(reset_db, input="n")

    assert result.exit_code == 0
    assert "[y/N]" in result.output
    assert "cancelled" in result.output


def test_init_superadmin(runner, app):
    with app.app_context():
        result = runner.invoke(init_superadmin, input="y")

    assert result.exit_code == 0
    assert "successfully" in result.output


def test_create_seed(runner, app):
    with app.app_context():
        result = runner.invoke(create_seed, ["--users", "1", "--groups", "1"])

    assert result.exit_code == 0
    assert "successfully" in result.output
