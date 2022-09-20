<div class="mermaid">
    classDiagram
    PInterface <|-- ProgressbarWriter : Implements
    SAbstraction <|-- Sector : Implements
    CInterface <|-- CalculationService : Implements
    SignatureSegment <-- Signature : Uses by default
    Signature --> PSProtocol : Matches
    SignatureSegment --> SSProtocol : Matches
    Sector --o ProgressbarWriter : By default
    CalculationService --o ProgressbarWriter : By default
    Signature --o ProgressbarWriter : By default
    PCInterface <|-- ProgressbarClient : Implements
    HInterface <|-- Hooks : Implements
    CMInterface <|-- ContractManager : Implements
    CMInterface --> ContractInterface : Interacts with
    Hooks --o ProgressbarClient : By default
    ContractManager --o ProgressbarClient : By default
    ProgressbarWriter --o ProgressbarClient : By default
</div>

::: multibar.settings
