import type { ProviderDriver, ProviderDriverRegistry } from "./provider_driver.js";

export class StaticProviderDriverRegistry implements ProviderDriverRegistry {
  private readonly driversByKey: Map<string, ProviderDriver>;

  constructor(drivers: ProviderDriver[] = []) {
    this.driversByKey = new Map(drivers.map((driver) => [driver.providerKey(), driver]));
  }

  all(): ProviderDriver[] {
    return Array.from(this.driversByKey.values());
  }

  find(providerKey: string): ProviderDriver | undefined {
    return this.driversByKey.get(providerKey);
  }
}
