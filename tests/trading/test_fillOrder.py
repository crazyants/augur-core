#!/usr/bin/env python

from ethereum.tools import tester
from utils import fix, bytesToHexString, captureFilteredLogs, longTo32Bytes, longToHexString
from constants import BID, ASK, YES, NO


def test_publicFillOrder_bid(contractsFixture, cash, market, universe):
    createOrder = contractsFixture.contracts['CreateOrder']
    fillOrder = contractsFixture.contracts['FillOrder']
    orders = contractsFixture.contracts['Orders']
    tradeGroupID = 42
    logs = []

    initialMakerETH = contractsFixture.chain.head_state.get_balance(tester.a1)
    initialFillerETH = contractsFixture.chain.head_state.get_balance(tester.a2)
    creatorCost = fix('2', '0.6')
    fillerCost = fix('2', '0.4')

    # create order
    orderID = createOrder.publicCreateOrder(BID, 2, fix('0.6'), market.address, YES, longTo32Bytes(0), longTo32Bytes(0), tradeGroupID, sender = tester.k1, value=creatorCost)

    # fill best order
    captureFilteredLogs(contractsFixture.chain.head_state, orders, logs)
    captureFilteredLogs(contractsFixture.chain.head_state, contractsFixture.contracts['Augur'], logs)
    fillOrderID = fillOrder.publicFillOrder(orderID, 2, tradeGroupID, sender = tester.k2, value=fillerCost)

    assert len(logs) == 5

    assert logs[4]["_event_type"] == "OrderFilled"
    assert logs[4]["filler"] == bytesToHexString(tester.a2)
    assert logs[4]["numCreatorShares"] == 0
    assert logs[4]["numCreatorTokens"] == creatorCost
    assert logs[4]["numFillerShares"] == 0
    assert logs[4]["numFillerTokens"] == fillerCost
    assert logs[4]["marketCreatorFees"] == 0
    assert logs[4]["reporterFees"] == 0
    assert logs[4]["shareToken"] == market.getShareToken(YES)
    assert logs[4]["tradeGroupId"] == 42

    assert contractsFixture.chain.head_state.get_balance(tester.a1) == initialMakerETH - creatorCost
    assert contractsFixture.chain.head_state.get_balance(tester.a2) == initialFillerETH - fillerCost
    assert orders.getAmount(orderID) == 0
    assert orders.getPrice(orderID) == 0
    assert orders.getOrderCreator(orderID) == longToHexString(0)
    assert orders.getOrderMoneyEscrowed(orderID) == 0
    assert orders.getOrderSharesEscrowed(orderID) == 0
    assert orders.getBetterOrderId(orderID) == longTo32Bytes(0)
    assert orders.getWorseOrderId(orderID) == longTo32Bytes(0)
    assert fillOrderID == 0

def test_publicFillOrder_ask(contractsFixture, cash, market, universe):
    createOrder = contractsFixture.contracts['CreateOrder']
    fillOrder = contractsFixture.contracts['FillOrder']
    orders = contractsFixture.contracts['Orders']
    tradeGroupID = 42
    logs = []

    initialMakerETH = contractsFixture.chain.head_state.get_balance(tester.a1)
    initialFillerETH = contractsFixture.chain.head_state.get_balance(tester.a2)
    creatorCost = fix('2', '0.4')
    fillerCost = fix('2', '0.6')

    # create order
    orderID = createOrder.publicCreateOrder(ASK, 2, fix('0.6'), market.address, YES, longTo32Bytes(0), longTo32Bytes(0), tradeGroupID, sender = tester.k1, value=creatorCost)

    # fill best order
    captureFilteredLogs(contractsFixture.chain.head_state, orders, logs)
    captureFilteredLogs(contractsFixture.chain.head_state, contractsFixture.contracts['Augur'], logs)
    fillOrderID = fillOrder.publicFillOrder(orderID, 2, tradeGroupID, sender = tester.k2, value=fillerCost)

    assert len(logs) == 5

    assert logs[4]["_event_type"] == "OrderFilled"
    assert logs[4]["filler"] == bytesToHexString(tester.a2)
    assert logs[4]["numCreatorShares"] == 0
    assert logs[4]["numCreatorTokens"] == creatorCost
    assert logs[4]["numFillerShares"] == 0
    assert logs[4]["numFillerTokens"] == fillerCost
    assert logs[4]["marketCreatorFees"] == 0
    assert logs[4]["reporterFees"] == 0
    assert logs[4]["shareToken"] == market.getShareToken(YES)
    assert logs[4]["tradeGroupId"] == 42

    assert contractsFixture.chain.head_state.get_balance(tester.a1) == initialMakerETH - creatorCost
    assert contractsFixture.chain.head_state.get_balance(tester.a2) == initialFillerETH - fillerCost
    assert orders.getAmount(orderID) == 0
    assert orders.getPrice(orderID) == 0
    assert orders.getOrderCreator(orderID) == longToHexString(0)
    assert orders.getOrderMoneyEscrowed(orderID) == 0
    assert orders.getOrderSharesEscrowed(orderID) == 0
    assert orders.getBetterOrderId(orderID) == longTo32Bytes(0)
    assert orders.getWorseOrderId(orderID) == longTo32Bytes(0)
    assert fillOrderID == 0

def test_publicFillOrder_bid_scalar(contractsFixture, cash, scalarMarket, universe):
    createOrder = contractsFixture.contracts['CreateOrder']
    fillOrder = contractsFixture.contracts['FillOrder']
    orders = contractsFixture.contracts['Orders']
    # We're testing the scalar market because it has a different numTicks than 10**18 as the other do. In particular it's numTicks is 40*18**18
    market = scalarMarket
    tradeGroupID = 42
    logs = []

    initialMakerETH = contractsFixture.chain.head_state.get_balance(tester.a1)
    initialFillerETH = contractsFixture.chain.head_state.get_balance(tester.a2)
    creatorCost = fix('2', '0.6')
    fillerCost = fix('2', '39.4')

    # create order
    orderID = createOrder.publicCreateOrder(BID, 2, fix('0.6'), market.address, YES, longTo32Bytes(0), longTo32Bytes(0), tradeGroupID, sender = tester.k1, value=creatorCost)

    # fill best order
    captureFilteredLogs(contractsFixture.chain.head_state, orders, logs)
    captureFilteredLogs(contractsFixture.chain.head_state, contractsFixture.contracts['Augur'], logs)
    fillOrderID = fillOrder.publicFillOrder(orderID, 2, tradeGroupID, sender = tester.k2, value=fillerCost)

    assert len(logs) == 5

    assert logs[4]["_event_type"] == "OrderFilled"
    assert logs[4]["filler"] == bytesToHexString(tester.a2)
    assert logs[4]["numCreatorShares"] == 0
    assert logs[4]["numCreatorTokens"] == creatorCost
    assert logs[4]["numFillerShares"] == 0
    assert logs[4]["numFillerTokens"] == fillerCost
    assert logs[4]["marketCreatorFees"] == 0
    assert logs[4]["reporterFees"] == 0
    assert logs[4]["shareToken"] == market.getShareToken(YES)
    assert logs[4]["tradeGroupId"] == 42

    assert contractsFixture.chain.head_state.get_balance(tester.a1) == initialMakerETH - creatorCost
    assert contractsFixture.chain.head_state.get_balance(tester.a2) == initialFillerETH - fillerCost
    assert orders.getAmount(orderID) == 0
    assert orders.getPrice(orderID) == 0
    assert orders.getOrderCreator(orderID) == longToHexString(0)
    assert orders.getOrderMoneyEscrowed(orderID) == 0
    assert orders.getOrderSharesEscrowed(orderID) == 0
    assert orders.getBetterOrderId(orderID) == longTo32Bytes(0)
    assert orders.getWorseOrderId(orderID) == longTo32Bytes(0)
    assert fillOrderID == 0
