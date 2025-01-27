from scripts.deploy import initialize_network, selectAccount, fund, withDraw, deploy

def test_Fund():
    # Arrange
    initialize_network()
    _Account = selectAccount()
    testContract = deploy(True, _Account)
    # Act
    fund(_Account, testContract, int(1 * 10**18))
    # Assert
    assert 10**18 == testContract.fundAmounts(_Account)
    withDraw(_Account, testContract)